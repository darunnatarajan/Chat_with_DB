# 🧠 MySQL Natural Language to SQL Chatbot using Groq LLM

This project converts natural language questions into syntactically correct MySQL queries using **Groq LLaMA-3**. It ensures schema-aware, validated SQL generation for business analysts, developers, and data teams.

---

## 🚀 Features

- 🗣️ Natural language to SQL via Groq API (LLaMA 3)
- 📚 Uses real database schema for accurate generation
- ✅ Validates SQL before execution (SELECT check, UNION mismatch, etc.)
- 🧪 Includes test cases to validate prompt accuracy
- 🔌 Modular structure for extensibility and future UI/API integration

---

## 🧱 Project Structure

```
mysql_nl_chatbot/
├── app.py                         # Main CLI chatbot interface
├── sql_generator.py               # Core logic to generate and validate SQL from prompts
├── prompt_builder.py              # Builds structured prompts for LLM using schema
├── schema_reader.py               # Loads schema info from DB or source
├── schema_formatter.py            # Formats schema as readable input for LLM
├── result_formatter.py            # Formats and prints SQL output
├── query_runner.py                # (Optional) Executes SQL on MySQL DB
├── test_question.py               # Automated prompt testing for robustness
├── test_mysql_connection.py       # Verifies DB connection setup
├── .env                           # Stores GROQ_API_KEY
├── .gitignore                     # Excludes pycache, .env, venv, etc.
├── requirements.txt               # All Python dependencies
├── README.md                      # This file
└── __pycache__/                   # Auto-generated Python cache files
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/darunnatarajan/Chat_with_DB.git
cd mysql_nl_chatbot
```

### 2. Create and Activate Virtual Environment (Optional but Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Your Groq API Key

Create a `.env` file:

```env
GROQ_API_KEY=your_actual_groq_api_key_here
```

---

## 🗄️ MySQL Schema Setup

Make sure your MySQL database includes the following tables and structure:

```sql
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    signup_date DATE
);

CREATE TABLE invoices (
    invoice_id INT PRIMARY KEY,
    subscription_id INT,
    invoice_date DATE,
    total_amount DECIMAL(10,2),
    tax_amount DECIMAL(10,2)
);

CREATE TABLE payments (
    payment_id INT PRIMARY KEY,
    invoice_id INT,
    payment_date DATE,
    amount_paid DECIMAL(10,2),
    payment_method VARCHAR(50)
);

CREATE TABLE subscriptions (
    subscription_id INT PRIMARY KEY,
    customer_id INT,
    plan_name VARCHAR(100),
    amount DECIMAL(10,2),
    start_date DATE,
    end_date DATE
);
```

---

## 💬 How to Use the CLI

```bash
python app.py
```

You’ll be prompted:

```
Ask a question in natural language (or type 'exit' to quit):
```

Example questions:

* "List all customers who joined after 2023"
* "Show total payments made for each invoice"
* "Get subscriptions that ended this year"

---

## 🧪 Run Prompt Test Suite

Run tests to validate common prompts and catch Groq output errors:

```bash
python test_question.py
```

This checks:

* Prompt-to-SQL generation
* Valid SELECT presence
* UNION column count mismatch
* Empty response detection

---

## 🔧 Key Modules Explained

* `sql_generator.py`: Sends prompt to Groq, cleans + validates SQL
* `prompt_builder.py`: Constructs LLM prompt using schema
* `test_question.py`: Runs a suite of prompt inputs and checks SQL output
* `schema_reader.py`: (Extensible) Can later pull schema from MySQL DB
* `query_runner.py`: (Optional) Executes SQL using `mysql-connector-python`
* `result_formatter.py`: Pretty prints or formats query output

---

## 🧠 Tips to Improve Accuracy

* Refine system prompt in `sql_generator.py` for stricter schema rules
* Add more edge case prompts in `test_question.py`
* Enable JOIN validation logic
* Implement fuzzy table/column matching warning

---

## 📌 Future Plans

* ✅ Streamlined schema loading from MySQL
* 🌐 Web interface using Streamlit or FastAPI
* 📈 SQL visualization / preview pane
* 🧩 Plugin architecture for Postgres or SQLite

---

## 🧑‍💻 Author

Built by [Darun Natarajan] – [[LinkedIn](https://www.linkedin.com/in/darunn/)]

---

## 📄 License

MIT License
