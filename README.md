# ModernDataAnalyticsProjectApp
This is the repository for application of the group project. It contains all the files necessary to run Plotly Dash application that is hosted on Heroku.

Link to the app: https://mda-croatia-2023.herokuapp.com/

Link to the main repository of the group project: https://github.com/IvanaOsredek/ModernDataAnalyticsProject/tree/main

## Description of the files
- **Procfile**: Contains commands that Heroku should execute to start and run the application.
- **app.py**: Main Python file that contains the code for the application. 
- **data.csv**: Dataframe with predictions from our final model. Application reads this file and displays predictions.
- **data_ref.csv**: Dataframe with reference values for average noise level. Application reads this file and displays reference.
- **requirements.txt**: Specifies necessary dependencies so that the application can be installed and run on Heroku platform.
