#################################### GETTING STARTED ####################################
# # Uncomment for new R user (custom installer like pip)
# source("usePackages.R")
# pkgnames <-
#   c(
#     "DT",
#     "DBI",
#     "reticulate",
#     "shiny",
#     "shinyjs",
#     "tidyverse",
#     "rsconnect",
#     "shinydashboard",
#     "shinydashboardPlus"
#   )
# loadPkgs(pkgnames)

library(DT)
library(DBI)
library(shiny)
library(shinyjs)
library(tidyverse)
library(rsconnect)
library(shinydashboard)
library(shinydashboardPlus)

PYTHON_DEPENDENCIES = c('pip','pandas')

#################################### VEVN SETUP FOR PYTHON ####################################

virtualenv_dir = Sys.getenv('VIRTUALENV_NAME')
python_path = Sys.getenv('PYTHON_PATH')

# Create virtual env and install dependencies
reticulate::virtualenv_create(envname = virtualenv_dir, python = python_path)
reticulate::virtualenv_install(virtualenv_dir, packages = PYTHON_DEPENDENCIES, ignore_installed=TRUE)
reticulate::use_virtualenv(virtualenv_dir, required = T)
reticulate::source_python("helper.py")

#################################### HELPER FUNCTIONS ####################################
# SQLite Connection
getDBConnection <- function() {
  conn <- dbConnect(RSQLite::SQLite(), dbname = "champion.db")
  conn
}

# Extract the tables from DB
getTeamInformation <- function() {
  conn <- getDBConnection()
  information <- dbReadTable(conn, "information")
  dbDisconnect(conn)
  information
}

getTeamMatches <- function() {
  conn <- getDBConnection()
  matches <- dbReadTable(conn, "matches")
  dbDisconnect(conn)
  matches
}

# Delete tables if exist for rerun
deleteTables <- function() {
  conn <- getDBConnection()
  dbSendQuery(conn, "DROP TABLE IF EXISTS champion.information;")
  dbSendQuery(conn, "DROP TABLE IF EXISTS champion.matches;")
  dbDisconnect(conn)
}

# Modal to show error if the user types a wrong format or empty text input
WronginputModal <- function() {
  div(id = "wronginputModal",
      modalDialog(
        easyClose = FALSE,
        title = strong("Error Message"),
        h5("Wrong text format!"),
        footer = tagList(modalButton(h5(strong(
          "Cancel"
        ))))
      ))
}

#################################### UI ####################################
ui <- dashboardPage(
  skin = "red",
  dashboardHeader(title = strong("Champions Web Application")),
  dashboardSidebar(
    sidebarMenu(id = "tabs",
                menuItem(strong("Input Text"), tabName = "start")),
    br(),
    tags$script(
      JS(
        "document.getElementsByClassName('sidebar-toggle')[0].style.visibility = 'hidden';"
      )
    ),
    textAreaInput(
      "team_info",
      "Team Information",
      value = "",
      placeholder = "(Example)\nteamA 01/04 1\nteamB 02/05 1\nteamC 03/06 1\nteamD 04/06 1",
      width = '100%',
      rows = 5,
      resize = "none"
    ),
    textAreaInput(
      "team_matches",
      "Match Results",
      value = "",
      placeholder = "(Example)\nteamA teamB 0 1\nteamA teamC 1 3\nteamA teamD 2 2\nteamA teamE 2 4",
      width = '100%',
      rows = 5,
      resize = "none"
    ),
    actionButton("check_valid",
                 h6(strong(
                   "Step 1: Check Valid Input"
                 )),
                 style = "color: #fff; background-color: #AE0404; border-color: #AE0404"),
    br(),
    actionButton("check_now",
                 h6(strong(
                   "Step 2: Run Evaluation"
                 )),
                 style = "color: #fff; background-color: #AE0404; border-color: #AE0404")
  ),
  dashboardBody(tabItems(tabItem(
    tabName = "start",
    fluidRow(
      useShinyjs(),
      class = "center",
      column(
        width = 12,
        h2(strong("Results of Evaluation")),
        tableOutput("table"),
        actionButton("clear_results",
                     h6(strong(
                       "Reset Everything"
                     )),
                     style = "color: #fff; background-color: #AE0404; border-color: #AE0404")
      )
    )
  )))
)

#################################### SERVER ####################################
server <- function(input, output, session) {
  
  # Initialize server values: Only the output table values
  vals <- reactiveValues(result_values = NULL)
  
  # Handle the reading of the multi-line text inputs and push to DB
  read_input_texts <- function(input_1, input_2) {
    # Try catch for invalid input handling
    tryCatch({
      # Add the multi-line inputs to data frames
      df_1 <- data.frame()
      df_2 <- data.frame()
      lines_1 <- unlist(str_split(input_1, "\n"))
      lines_2 <- unlist(str_split(input_2, "\n"))
      
      for (line in lines_1) {
        words <- unlist(str_split(line, " "))
        df_1 <- rbind(df_1, words)
      }
      for (line in lines_2) {
        words <- unlist(str_split(line, " "))
        df_2 <- rbind(df_2, words)
      }
      
      # Remove any empty words
      df_1 <- df_1[!apply(df_1 == "", 1, all), ]
      df_2 <- df_2[!apply(df_2 == "", 1, all), ]
      
      # Write to DB
      conn <- getDBConnection()
      dbWriteTable(conn,
                   "information",
                   df_1,
                   overwrite = TRUE,
                   row.names = FALSE)
      dbWriteTable(conn,
                   "matches",
                   df_2,
                   overwrite = TRUE,
                   row.names = FALSE)
      dbDisconnect(conn)
    },
    error = function(e) {
      showModal(WronginputModal())
    })
  }
  
  # Proceed to check the validity of the input texts
  observeEvent(input$check_valid, {
    read_input_texts(input$team_info, input$team_matches)
  })
  
  # Proceed with evaluation and output the results
  observeEvent(input$check_now, {
    information <- getTeamInformation()
    matches <- getTeamMatches()
    
    # convert 3rd column of information to double
    information[, 3] <- as.numeric(information[, 3])

    # convert 3rd and 4th column of matches to double
    matches[, 3] <- as.numeric(matches[, 3])
    matches[, 4] <- as.numeric(matches[, 4])
    
    vals$result_values <- get_rankings(information, matches)
    output$table <- renderTable(vals$result_values)
  })
  
  # Proceed to reset everything
  observeEvent(input$clear_results, {
    updateTextInput(session, "team_info", value = "")
    updateTextInput(session, "team_matches", value = "")
    vals$result_values <- NULL
    deleteTables()
  })
}

shinyApp(ui, server)
