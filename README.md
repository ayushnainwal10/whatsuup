# WhatsApp Chat Analyzer

This is a Python-based application built using Streamlit for analyzing and visualizing WhatsApp chat data.

## Overview

WhatsApp Chat Analyzer is a tool designed to parse and analyze chat data exported from WhatsApp. With this application, users can gain insights into their chat history, including message frequency, word counts, most active users, and more. The application provides an interactive interface for exploring the data and generating visualizations.

## Features

- **Import WhatsApp Chat:** Upload your exported WhatsApp chat text file (.txt) to analyze.

- **Message Statistics:** View statistics such as total messages, average message length, most active users, and message frequency over time.
  ![WhatsApp Chat Analyzer](/images/img1.png)
  
- **Word Cloud:** Generate a word cloud to visualize the most commonly used words in the chat.
  ![WhatsApp Chat Analyzer](/images/img6.png)

- **Timeline Analysis:** Explore message frequency trends over time using an interactive timeline chart.
  ![WhatsApp Chat Analyzer](/images/img2.png)

- **Heatmap** nteractive heatmap visualization showcasing message frequency and activity patterns over time in WhatsApp conversations.
  ![WhatsApp Chat Analyzer](/images/img5.png)

- **Export Data:** Export analyzed data and visualizations for further analysis or sharing.



## Installation

To run the WhatsApp Chat Analyzer locally, follow these steps:

1. Clone this repository to your local machine.
2. Install the required dependencies using pip:
    ```
    pip install -r requirements.txt
    ```
3. Run the Streamlit application:
    ```
    streamlit run app.py
    ```

## Usage

1. Launch the application by running the Streamlit command.
2. Upload your exported WhatsApp chat text file (.txt).
3. Explore the various tabs to view different analyses and visualizations.
4. Interact with the charts and filters to customize your analysis.
5. Export the generated visualizations or download the analyzed data for further use.

## Deployment

This application is deployed on Render for easy access. You can access the deployed version [here](https://whatsapp-chat-analyzer-86az.onrender.com/).

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.
