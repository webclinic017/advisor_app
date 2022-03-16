import yagmail
from datetime import datetime



class The_Only_Mailer(object):


    def __init__(self, today):
        self.today_stamp = str(today)
        self.saveMonth = str(today)[:7]


    def mail_em_out(self):
        mailer = yagmail.SMTP(user="the.only.game.in.town.011235813@gmail.com", password="01905040")

        recipient_lst = [
            "gordon.pisciotta@gmail.com",
        ]

        subject = "Welcome to the Matrix"

        content_lst = ["Wake up Neo...", "Follow the white rabbit"]

        attachments_lst=[
            '/home/gordon/modern_millennial_market_mapping/reports/port_results/2021-09/2021-09-23/maximum_sharpe_ratio_best.csv',
            '/home/gordon/modern_millennial_market_mapping/reports/port_results/2021-09/2021-09-23/maximum_sharpe_ratio_portfolio_equalWT.csv',
            '/home/gordon/modern_millennial_market_mapping/reports/port_results/2021-09/2021-09-23/maximum_sharpe_ratio_portfolio_random.csv',
            '/home/gordon/modern_millennial_market_mapping/reports/port_results/2021-09/2021-09-23/minimum_volatility_portfolio_best.csv',
        ]        

        cc_lst=[
            "gdp011235@gmail.com",
            "gdp@the.only.game.in.town.net",
            "jayci.miltenberger@gmail.com",                
        ]

        mailer.send(
            to=recipient_lst,
            subject=subject,
            contents=content_lst,
            attachments=attachments_lst,
            cc=cc_lst
        )

        print("Report Emailed [COMPLETE]")


if __name__ == "__main__":
    The_Only_Mailer(str(datetime.now())[:10]).mail_em_out()
