from genericpath import exists
import yagmail
from datetime import datetime


class The_Only_Mailer(object):
    def __init__(self, today):
        self.today_stamp = str(today)
        self.saveMonth = str(today)[:7]

    def mail_em_out(self):
        mailer = yagmail.SMTP(
            user="the.only.game.in.town.011235813@gmail.com", password="01905040"
        )

        subject = "Welcome to the (stock) Matrix"
        content_lst = ["Wake up Neo...", "Follow the white rabbit"]
        recipient_lst = ["gordon.pisciotta@gmail.com"]
        cc_lst = [
            "gdp011235@gmail.com",
            "gordon.pisciotta@gmail.com",
            # "jayci.miltenberger@gmail.com",
            # "zach.steinbaugh@gmail.com",
            # "agriffeyhaack@gmail.com",
            # "rkanaley@variantequity.com",
            # "dean@racapitalinc.com",
            
        ]

        if exists(
            f"/home/gdp/invest_4m/reports/port_results/{self.saveMonth}/{self.today_stamp}/maximum_sharpe_ratio.csv"
        ):
            try:
                attachments_lst = [
                    f"/home/gdp/invest_4m/reports/port_results/{self.saveMonth}/{self.today_stamp}/maximum_sharpe_ratio.csv",
                    f"/home/gdp/invest_4m/reports/port_results/{self.saveMonth}/{self.today_stamp}/maximum_sharpe_equalWT.csv",
                    # f"/home/gdp/invest_4m/reports/port_results/{self.saveMonth}/{self.today_stamp}/markowitz_random.csv",
                    f"/home/gdp/invest_4m/reports/port_results/{self.saveMonth}/{self.today_stamp}/minimum_volatility_portfolio.csv",
                    f"/home/gdp/invest_4m/reports/port_results/{self.saveMonth}/{self.today_stamp}/monte_carlo_cholesky.csv",
                ]
            except:
                pass

        elif exists(
            f"/home/gordon/invest_4m/reports/port_results/{self.saveMonth}/{self.today_stamp}/maximum_sharpe_ratio.csv"
        ):
            try:
                attachments_lst = [
                    f"/home/gordon/invest_4m/reports/port_results/{self.saveMonth}/{self.today_stamp}/maximum_sharpe_ratio.csv",
                    f"/home/gordon/invest_4m/reports/port_results/{self.saveMonth}/{self.today_stamp}/maximum_sharpe_equalWT.csv",
                    # f"/home/gordon/invest_4m/reports/port_results/{self.saveMonth}/{self.today_stamp}/markowitz_random.csv",
                    f"/home/gordon/invest_4m/reports/port_results/{self.saveMonth}/{self.today_stamp}/minimum_volatility_portfolio.csv",
                    f"/home/gordon/invest_4m/reports/port_results/{self.saveMonth}/{self.today_stamp}/monte_carlo_cholesky.csv",
                ]
            except:
                pass

        elif exists(
            f"/home/gdp/invest_4m/reports/port_results/{self.saveMonth}/{self.today_stamp}/maximum_sharpe_ratio.csv"
        ):
            try:
                attachments_lst = [
                    f"/home/gdp/invest_4m/reports/port_results/{self.saveMonth}/{self.today_stamp}/maximum_sharpe_ratio.csv",
                    f"/home/gdp/invest_4m/reports/port_results/{self.saveMonth}/{self.today_stamp}/maximum_sharpe_equalWT.csv",
                    # f"/home/gdp/invest_4m/reports/port_results/{self.saveMonth}/{self.today_stamp}/markowitz_random.csv",
                    f"/home/gdp/invest_4m/reports/port_results/{self.saveMonth}/{self.today_stamp}/minimum_volatility_portfolio.csv",
                    f"/home/gdp/invest_4m/reports/port_results/{self.saveMonth}/{self.today_stamp}/monte_carlo_cholesky.csv",
                ]
            except:
                pass

        mailer.send(
            to=recipient_lst,
            subject=subject,
            contents=content_lst,
            attachments=attachments_lst,
            cc=cc_lst,
        )

        print(f"Final Report For Today {self.today_stamp} [EMAILS COMPLETE]")


if __name__ == "__main__":
    The_Only_Mailer("2021-10-15").mail_em_out()
