import pyodbc
import pandas as pd
import smtplib

class DatabaseConnector:
    def __init__(self, server, database):
        self.server = server
        self.database = database
        self.cnxn = None

    def connect(self):
        try:
            self.cnxn = pyodbc.connect(f"Driver={{SQL Server Native Client 11.0}};"
                                        f"Server={self.server};"
                                        f"Database={self.database};"
                                        f"Trusted_Connection=yes;")
            print("Connected to the database.")
        except Exception as e:
            print(f"Error connecting to the database: {e}")

    def execute_query(self, sql_query):
        try:
            df = pd.read_sql_query(sql_query, self.cnxn, index_col="TimeStamp", parse_dates=True)
            return df
        except Exception as e:
            print(f"Error executing query: {e}")
            return pd.DataFrame()

class MailSender:
    def __init__(self, sender_email, sender_password, smtp_server, smtp_port=25):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

    def send_mail(self, receiver_email, subject, body):
        message = f'Subject: {subject}\n\n{body}'
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, receiver_email, message)
            server.quit()
            print("Mail sent successfully.")
        except Exception as e:
            print(f"Error sending email: {e}")

def main():
    server = "na0vm00024.apac.bosch.com"
    database = "DB_MFC2DB_SQL"
    sql_query = """SELECT [CoolantPr], [ToolBroken], [TimeStamp], 'dz1' AS dz
         FROM [ChironDZ1]
         WHERE [TimeStamp] >= DATEADD(MINUTE, -6, GETDATE()) 
         AND [ToolBroken] = 0
         AND [ProgRun] = 1

         UNION

         SELECT [CoolantPr], [ToolBroken], [TimeStamp], 'dz2' AS dz
         FROM [ChironDZ2]
         WHERE [TimeStamp] >= DATEADD(MINUTE, -6, GETDATE()) 
         AND [ToolBroken] = 0
         AND [ProgRun] = 1
         
         UNION

         SELECT [CoolantPr], [ToolBroken], [TimeStamp], 'dz3' AS dz
         FROM [ChironDZ3]
         WHERE [TimeStamp] >= DATEADD(MINUTE, -6, GETDATE()) 
         AND [ToolBroken] = 0
         AND [ProgRun] = 1
         
         UNION

         SELECT [CoolantPr], [ToolBroken], [TimeStamp], 'dz4' AS dz
         FROM [ChironDZ4]
         WHERE [TimeStamp] >= DATEADD(MINUTE, -6, GETDATE()) 
         AND [ToolBroken] = 0
         AND [ProgRun] = 1
         
         UNION

         SELECT [CoolantPr], [ToolBroken], [TimeStamp], 'dz6' AS dz
         FROM [ChironDZ6]
         WHERE [TimeStamp] >= DATEADD(MINUTE, -6, GETDATE()) 
         AND [ToolBroken] = 0
         AND [ProgRun] = 1
         
         UNION

         SELECT [CoolantPr], [ToolBroken], [TimeStamp], 'dz7' AS dz
         FROM [ChironDZ7]
         WHERE [TimeStamp] >= DATEADD(MINUTE, -6, GETDATE()) 
         AND [ToolBroken] = 1
         AND [ProgRun] = 1
         
         UNION

         SELECT [CoolantPr], [ToolBroken], [TimeStamp], 'dz8' AS dz
         FROM [ChironDZ8]
         WHERE [TimeStamp] >= DATEADD(MINUTE, -6, GETDATE()) 
         AND [ToolBroken] = 0
         AND [ProgRun] = 1
         
         UNION

         SELECT [CoolantPr], [ToolBroken], [TimeStamp], 'dz9' AS dz
         FROM [ChironDZ9_1]
         WHERE [TimeStamp] >= DATEADD(MINUTE, -6, GETDATE()) 
         AND [ToolBroken] = 0
         AND [ProgRun] = 1
         
         
         ORDER BY [TimeStamp] ASC"""

    db_connector = DatabaseConnector(server, database)
    db_connector.connect()
    df = db_connector.execute_query(sql_query)

    if not df.empty:
        mail_sender = MailSender("chs9na@bosch.com", "Welcome@Nashik2", "rb-smtp-auth.rbesz01.com")
        subject = "Testing"
        body = f"Tool Broken Status at ChironDZ Machines : {df['dz'].unique()}"
        mail_sender.send_mail("chs9na@bosch.com", subject, body)
    else:
        print("No problem.")

if __name__ == "__main__":
    main()
