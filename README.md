# spotify-end-to-end-data_engineering-project - Top Songs in Japan


## Project Overview
This project involves developing an ETL (Extract, Transform, Load) pipeline using AWS services to collect and process data from the "Top Songs in Japan" playlist on Spotify. The goal is to automate the extraction of music data, transform it into structured formats, and store it in AWS for further analysis. The data is organized into separate tables for albums, artists, and songs, which can be visualized using tools like Power BI and Tableau for dashboard analytics.

## Key Components

### Data Extraction:
- **Spotify API**: Retrieve music data, including track details, artist information, and albums, using the Spotify API.
- **Authentication**: Implement OAuth 2.0 for secure access to the Spotify API.
- **Scheduling**: Use Amazon CloudWatch to trigger the pipeline on a daily basis to automatically extract the latest data using Cron syntax

### Data Transformation:
- **Data Cleaning**: Cleanse the raw data by handling missing values, duplicates, and inconsistencies.
- **Data Formatting**: Transform the data into structured formats (e.g., JSON or CSV) for compatibility with downstream processes.
- **Enrichment**: Add additional attributes or aggregate information to enhance the data for analysis.

### Data Loading:
- **AWS S3**: Store both raw and processed data in AWS S3 for scalable and cost-effective storage.
- **AWS Glue**: Use AWS Glue and Crawler to infer schemas and create tables within the database.
- **AWS Athena**: Perform SQL analytics on the processed data stored in S3.
- **Data Partitioning**: Organize data into partitions based on attributes like date or category to optimize query performance.

## Workflow
1. **Extract**: The pipeline periodically calls the Spotify API to fetch the latest music data from the Top Songs in Japan playlist.
2. **Transform**: The raw data is cleaned, formatted, and enriched to meet the analysis requirements.
3. **Load**: The processed data is uploaded to AWS S3 and stored in partitioned formats. AWS Glue is used for schema inference and table creation, while AWS Athena is used for SQL-based analytics.

## Analytics Use Cases:
- **Artist Analysis**: Analyze top-performing artists by counting their appearances in the playlist, and explore trends over time.
- **Album Analysis**: Track the most popular albums and how often songs from each album appear in the playlist.
- **Song Popularity**: Measure song popularity through attributes like the number of streams, artist performance, or song genre.
- **Time Series Analysis**: Investigate trends in song popularity by analyzing data over different time periods (e.g., weekly, monthly).

## Tools and Technologies:
- **AWS Services**: AWS Lambda, AWS S3, AWS Glue, Amazon CloudWatch, AWS Athena
- **Programming Languages**: Python (for API interactions and ETL scripting)
- **Libraries**: `spotipy` (for Spotify API interactions), `pandas` (for data manipulation), `boto3` (for interacting with AWS services)
- **Visualization Tools**: Power BI, Tableau

## Benefits:
- **Automation**: The ETL pipeline automates the entire data processing workflow, reducing manual effort and ensuring up-to-date data.
- **Scalability**: Using AWS services ensures the solution can scale to handle large volumes of data efficiently.
- **Flexibility**: The modular design allows for easy integration with other data sources and analytics tools.

## How to Use:
1. Clone the repository to your local machine.
2. Configure the Spotify API credentials and AWS environment.
3. Set up CloudWatch triggers to automate the pipeline.
4. Run the pipeline to start collecting and transforming data.
5. Query the data in Athena or visualize it with Power BI/Tableau.

## Future Enhancements:
- **Advanced Analytics**: Implement machine learning models to predict song popularity or detect trends in music genres.
- **Real-Time Streaming**: Consider transitioning to a real-time streaming solution to process live data from Spotify.


