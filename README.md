# Text-Summarization-Website

## Description:
The Summarizer Web Application is a Flask-based web application that allows users to input articles, summarize them using text summarization techniques, and save the summaries along with quality metrics such as readability, compression ratio, and keyword density.

## Installation:
first to install the dataset i cloned the repository to the local machine. Then, load the dataset.

## Setting Up Environmental Variables:
configured essential environment variables such as SECRET_KEY and SQLALCHEMY_DATABASE_URI. These variables are crucial for the proper functioning of the Flask application. Make any necessary updates to app.py as needed.

## Functionality Overview:
### 1. User Authentication: 
Allows users to register for an account or log in using existing credentials securely.
### 2. Summarization: 
Provides options to input articles directly or upload files for summarization. Users can choose between brief or detailed summaries based on their preferences.
### 3. Quality Metrics:
Computes and displays readability scores, compression ratios, and keyword densities for generated summaries.
### 4. Save and Retrieve Summaries: 
Enables users to save their summaries to their account for future reference and review.

## Technologies used:
### 1. Flask: 
A lightweight and versatile Python web framework used for building the application's backend and routing.
### 2. SQLAlchemy:
An Object-Relational Mapping (ORM) library for Python that facilitates database management and interaction.
### 3.Chart.js:
A JavaScript library for creating responsive and visually appealing charts, utilized here to visualize quality metrics.
### 4. Sumy: 
A Python library specialized in text summarization, offering various algorithms such as LSA (Latent Semantic Analysis).
#### 5. Bootstrap:
A popular front-end framework for developing responsive and mobile-first websites, used for styling and UI components.

## User Functionality
The Summarizer Web Application offers several user-centric functionalities designed to enhance user experience and interaction. Upon accessing the application, users are prompted to either log in or register if they don't have an account. The login functionality securely validates user credentials against those stored in the SQLite database using hashed passwords for security. Registered users can save their summaries for future reference, view their saved summaries in the "My Summaries" section

## 1. Summarization Functionality
The core functionality of the application revolves around text summarization. Users can input articles directly into a text area or upload files for summarization. The summarization process employs advanced Natural Language Processing (NLP) techniques, specifically Latent Semantic Analysis (LSA), to generate concise summaries based on user preferences. The application provides options for both brief and detailed summaries, adjusting the summarization ratio accordingly. Additionally, it calculates and displays key metrics such as readability score, compression ratio, and keyword density to assess the quality and relevance of the summaries produced.

## 2. Metric Calculation
To evaluate the effectiveness of the summarization process, the application calculates three main metrics: readability, compression ratio, and keyword density. These metrics provide valuable insights into the clarity, conciseness, and focus of the summarized content. Readability is assessed using the Flesch Reading Ease score, while compression ratio compares the length of the original text to the length of the summarized text. Keyword density measures the concentration of important terms in the summary relative to the overall word count. These metrics collectively help users gauge the efficiency and accuracy of the summarization process.

## 3. Image Generation
In addition to textual summaries, the application offers a feature to generate corresponding visual representations of the summaries. This functionality utilizes an external API, such as Google's Imagen 3 service, to create images that visually encapsulate the essence of the summarized content. Users can initiate image generation directly from the application interface after summarizing an article, enhancing the accessibility and multimedia integration of the summarized information.

## 4. Navigation and Interface
The application's interface is designed to be intuitive and user-friendly, featuring navigation elements such as a navbar that dynamically adjusts based on the user's authentication status. For authenticated users, the navbar provides links to the main summarization functionality, saved summaries, and logout options. Conversely, guests are directed to login or registration pages, facilitating seamless interaction and personalized user experiences based on authentication status.


