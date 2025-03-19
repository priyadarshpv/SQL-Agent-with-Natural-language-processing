# NL2SQL Agent: Natural Language to SQL Query Generator

**NL2SQL Agent** is a powerful tool that enables users to interact with SQL databases using natural language. It leverages state-of-the-art language models (LLMs) to convert natural language queries into SQL queries, executes them on a MySQL database, and returns the results in a user-friendly format. This project is built using the **LangChain framework** and integrates with the **Groq API** for natural language processing.

---

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Technical Architecture](#technical-architecture)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Contributing](#contributing)
7. [License](#license)

---

## Overview

The **NL2SQL Agent** bridges the gap between non-technical users and relational databases by allowing them to query databases using plain English (or other natural languages). It is designed to:
- **Understand Natural Language**: Accept user queries in natural language (e.g., "Show me all customers from New York").
- **Generate SQL Queries**: Convert natural language queries into valid SQL queries using a language model.
- **Execute Queries**: Run the generated SQL queries on a MySQL database.
- **Return Results**: Display the query results in a structured and readable format.

This project is ideal for:
- Data analysts who want to simplify database interactions.
- Developers building conversational interfaces for databases.
- Organizations looking to democratize data access for non-technical users.

---

## Features

- **Natural Language to SQL Conversion**:
  - Converts natural language queries into SQL queries using the **Groq API** and **LangChain**.
  - Supports SELECT, INSERT, UPDATE, and DELETE queries.
- **Database Interaction**:
  - Connects to MySQL databases and executes SQL queries.
  - Handles both read (SELECT) and write (INSERT, UPDATE, DELETE) operations.
- **Error Handling**:
  - Validates SQL queries before execution to prevent errors.
  - Provides informative error messages for invalid queries or database issues.
- **User-Friendly Output**:
  - Formats query results as tables for easy readability.
- **Extensible Design**:
  - Built using modular components, making it easy to extend or integrate with other systems.

---

## Technical Architecture

The NL2SQL Agent is built using the following components:

1. **Natural Language Processing (NLP)**:
   - Uses the **Groq API** with the `mixtral-8x7b-32768` model for natural language understanding and SQL generation.
   - Leverages **LangChain** for prompt engineering and query generation.

2. **Database Interaction**:
   - Connects to MySQL databases using the `mysql-connector-python` library.
   - Executes SQL queries and fetches results using a custom `execute_sql_query` tool.

3. **Agent Framework**:
   - Uses LangChain's **zero-shot ReAct agent** to orchestrate the workflow.
   - Combines reasoning (generating SQL queries) and acting (executing queries) to solve user tasks.

4. **Validation and Error Handling**:
   - Validates SQL queries using the `sqlparse` library.
   - Handles database errors gracefully and provides informative feedback.

5. **User Interface**:
   - Command-line interface (CLI) for interacting with the agent.
   - Easy-to-follow prompts for table names and natural language queries.

---

## Installation

### Prerequisites
- Python 3.8 or higher.
- A MySQL database.
- A Groq API key (sign up at [Groq](https://groq.com/)).

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/nl2sql-agent.git
   cd nl2sql-agent
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root and add your credentials:
   ```env
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_password
   DB_NAME=health
   GROQ_API_KEY=your_groq_api_key
   ```

4. Run the script:
   ```bash
   python main.py
   ```

---

## Usage

1. Start the NL2SQL Agent:
   ```bash
   python main.py
   ```

2. Enter the table name when prompted:
   ```
   Enter the table name: customers
   ```

3. Enter your query in natural language:
   ```
   Enter your query in natural language: Show me all customers from New York
   ```

4. View the results:
   - The agent will generate and execute the SQL query.
   - The results will be displayed in a tabular format.

### Example
```
Enter the table name: orders
Enter your query in natural language: Show me the total revenue for each product
Generated SQL Query: SELECT product_id, SUM(revenue) AS total_revenue FROM orders GROUP BY product_id;
Query Result:
   product_id  total_revenue
0           1         2500.0
1           2         1800.0
```

---

## Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and push to the branch.
4. Open a pull request with a detailed description of your changes.

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments
- **LangChain**: For providing the framework to build and orchestrate agents.
- **Groq**: For the powerful language model used for natural language processing.
- **MySQL**: For the reliable and scalable database system.


### **Key Highlights**
1. **Technical Project Name**: The project is named **NL2SQL Agent** to reflect its core functionality (Natural Language to SQL).
2. **Elaborate Overview**: Provides a detailed description of the project's purpose, target audience, and use cases.
3. **Technical Architecture**: Explains the components and technologies used in the project.
4. **Installation and Usage**: Includes clear, step-by-step instructions for setting up and using the project.
5. **Contributing and License**: Encourages contributions and specifies the license.

This `README.md` file is designed to make your project stand out on GitHub and provide all the necessary information for users and contributors.
