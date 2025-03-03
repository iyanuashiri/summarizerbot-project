# summarizerbot-project


# Twitter Summarizer Bot

A Twitter bot system that automatically summarizes articles shared in tweets when mentioned, built with a microservices architecture deployed on AWS.

## Overview

This project creates a Twitter bot that listens for mentions, detects shared URLs in those mentions, generates summaries of the linked articles, and replies to the user with a link to view the summary. The system is built as a collection of microservices that work together to provide this functionality.

## Project Status

**Note:** This project is no longer actively maintained or operated. Following Elon Musk's acquisition of Twitter (now X), the platform implemented significant changes to their API pricing structure in 2023. The previously free API access became a paid service with substantial costs, making the continued operation of this bot financially unsustainable for a personal/portfolio project. The codebase remains available as a demonstration of architecture and implementation but would require updates to work with current Twitter API policies and pricing.

## Value Proposition

This project demonstrates expertise in several high-demand areas of modern software development:

- **Microservices Architecture**: Showcases the ability to design and implement loosely coupled services
- **Cloud-Native Development**: Leverages AWS serverless and container technologies
- **DevOps Practices**: Implements infrastructure as code and CI/CD pipelines
- **ML/NLP Integration**: Demonstrates practical application of natural language processing
- **API Integration**: Shows proficiency with external APIs (Twitter) and internal service communication
- **Full-Stack Development**: Combines backend services with a web frontend

## Architecture

The project uses a microservices architecture with the following components:

```
├── get_mentions       # Lambda service that detects Twitter mentions
├── summarizer_ml      # ML service that generates article summaries
├── create_summaries   # Lambda service that stores summaries in the database
├── summarizer_bot     # Twitter bot service that replies to users
├── summarizer_web     # Web application to display summaries
└── summarizer-devops  # Infrastructure as code for AWS deployment
```

## Technical Showcase

This project demonstrates technical proficiency in:

- **Python Ecosystem**: Flask, NLTK, asyncio, Tweepy
- **AWS Services**: Lambda, ECR, S3, App Runner
- **Infrastructure as Code**: Pulumi for AWS resource management
- **Containerization**: Docker for service packaging and deployment
- **Database Design**: SQL database with migrations
- **Asynchronous Processing**: Event-driven architecture with async handlers
- **API Design**: RESTful endpoints for service communication
- **Web Development**: HTML/CSS/JS frontend with Flask templating

## How It Works

1. **Mention Detection**: Monitors Twitter for mentions of the bot account
2. **URL Extraction**: Identifies URLs in the mentioned tweets
3. **Article Processing**: Fetches and summarizes the article content
4. **Summary Storage**: Stores the summary in a database
5. **User Response**: Replies to the user with a link to view the summary
6. **Web Interface**: Provides a web page to view the saved summaries

## Components

### get_mentions

This Lambda function monitors Twitter for mentions of the bot account. It uses the Twitter API to retrieve mentions and extracts URLs from the referenced tweets.

- **Key Features**:
  - Uses Tweepy to interact with the Twitter API
  - Tracks mentions since the last check using Redis
  - Extracts URLs from referenced tweets
  - Generates unique IDs for each mention
  - Implements error handling for API rate limits and connection issues

### summarizer_ml

This service uses natural language processing to generate summaries of articles. It leverages NLTK for text processing and extraction.

- **Key Features**:
  - Uses NLTK for text tokenization and processing
  - Provides extractive summarization of article content
  - Implements smart text analysis algorithms
  - Optimizes for processing speed in serverless environment
  - Handles various article formats and structures

### create_summaries

This Lambda function stores the generated summaries in a database via the web application's API.

- **Key Features**:
  - Receives summary data from the summarizer_ml service
  - Sends POST requests to the web application's API
  - Uses asyncio for concurrent processing
  - Implements retry logic for failed requests
  - Validates data before storage

### summarizer_bot

This service handles the bot's interactions with Twitter users, responding to mentions with links to view the generated summaries.

- **Key Features**:
  - Uses Tweepy to post replies to users
  - Creates tweets with links to the summary web pages
  - Handles Twitter API rate limiting and error scenarios
  - Implements smart reply formatting
  - Manages conversation threading

### summarizer_web

A Flask web application that provides the user interface for viewing article summaries.

- **Key Features**:
  - REST API endpoints for creating and retrieving summaries
  - Database integration using SQLAlchemy
  - Web pages for viewing summaries
  - Supports user authentication and management
  - Database migrations with Alembic
  - Error handling and logging
  - Responsive design for mobile and desktop

### summarizer-devops

Infrastructure as code for deploying the services on AWS using Pulumi.

- **Key Features**:
  - Defines AWS resources including Lambda, ECR, S3, and App Runner
  - Manages deployments across environments (dev/prod)
  - Handles resource provisioning and configuration
  - Implements security best practices
  - Optimizes for cost efficiency

## Deployment

The project is containerized using Docker and deployed on AWS. Each component is packaged as a Docker container and deployed to its respective service:

- Lambda functions for event-driven processing
- ECR for container registry
- S3 for static assets
- App Runner for the web application

## Environment Variables

The following environment variables are required for the project:

### Twitter API Credentials
- `TWITTER_CONSUMER_KEY`
- `TWITTER_CONSUMER_SECRET`
- `TWITTER_ACCESS_TOKEN`
- `TWITTER_ACCESS_TOKEN_SECRET`
- `TWITTER_USERNAME`
- `TWITTER_USERNAME_ID`
- `TWITTER_BEARER_TOKEN`

### Redis Configuration
- `REDIS_PASSWORD_DEV`
- `REDIS_PORT_DEV`
- `REDIS_HOST_DEV`
- `REDIS_PASSWORD_PROD`
- `REDIS_PORT_PROD`
- `REDIS_HOST_PROD`

### Application Configuration
- `POST_URL` - URL for posting summaries
- `DOMAIN_URL` - Base domain for the web application
- `CURRENT_ENV` - Current environment (development/production)
- `SINCE_ID` - Twitter ID to track mentions since

## Local Development

To run the project locally:

1. Install Docker and Docker Compose
2. Clone the repository
3. Create a `.env` file with the required environment variables
4. 

## Getting Started

1. Set up a Twitter Developer account and create an application
2. Configure the required environment variables
3. Deploy the infrastructure using Pulumi
4. Start monitoring for mentions

## Database Migration

The project uses Alembic for database migrations:

```bash
cd summarizer_web
flask db init     # Only for the first time
flask db migrate  # Create migration
flask db upgrade  # Apply migration
```

## Scalability Considerations

The architecture is designed for scalability:

- **Stateless Services**: All components can scale horizontally
- **Event-Driven Processing**: Asynchronous communication allows for better load handling
- **Serverless Functions**: Auto-scaling based on demand
- **Database Optimization**: Efficient queries and indexing

## Impact of Twitter API Changes

When this project was initially developed, Twitter offered free API access with reasonable rate limits, making it viable to operate bots like this one at minimal cost. In early 2023, following Elon Musk's acquisition of Twitter, the platform implemented a new pricing structure that:

- Eliminated free API access tiers
- Introduced significant monthly fees for basic API access (starting at $100/month)
- Restricted the types of operations available at each pricing tier
- Reduced rate limits for many API endpoints

These changes fundamentally altered the economics of operating Twitter bots for personal or small-scale projects. The costs of maintaining API access for this bot would have exceeded $1,200 annually just for basic functionality, not including the AWS infrastructure costs to run the services.

As a result, this project was discontinued as an active service but remains as a portfolio demonstration of distributed systems architecture and NLP implementation.

## Future Enhancements

Potential improvements that could be implemented if the project were revived:

- **Enhanced Summarization**: Implement transformer-based models (BERT, GPT) for improved summaries
- **User Preferences**: Allow users to customize summary length and style
- **Analytics Dashboard**: Track usage patterns and popular content
- **Multi-language Support**: Expand summarization to additional languages
- **Content Classification**: Categorize articles by topic
- **Readability Metrics**: Provide additional insights about article complexity
- **Platform Migration**: Adapt the system to work with other social media platforms with more favorable API policies

## Professional Development Value

This project demonstrates several valuable skills for career advancement:

- **System Design**: Complex distributed system architecture
- **Cloud Architecture**: AWS service integration and optimization
- **Natural Language Processing**: Practical application of NLP techniques
- **API Development**: RESTful service design and implementation
- **Infrastructure Management**: IaC and deployment automation
- **Event-Driven Programming**: Asynchronous and reactive patterns
- **Adaptation to API Changes**: Understanding the impact of third-party API changes on business viability

## License

This project is licensed under the terms found in the LICENSE file in the root of this repository.

## Contributing

While the project is no longer actively maintained, the codebase remains open for educational purposes. If you're interested in adapting it to work with current Twitter API policies or other platforms, contributions are welcome! Please feel free to submit a Pull Request.



1. gunicorn 'summarizerbot:create_app()' --bind 0.0.0.0:5000

2. flask run
3. docker build -t summarizer-web .
4. docker run -d -p 5000:5000 summarizer-web
5. docker compose up --build


1. flask db init
2. flask db migrate -m "---"
3. flask db upgrade