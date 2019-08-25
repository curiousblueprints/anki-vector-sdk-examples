from simple_salesforce import Salesforce
import anki_vector

def main():

    connection = Salesforce(username='cameron@theamesfamily.net.vector', password='caliber2018VT!', security_token='vcqv01lqqMFuLgrJa0BptGDP')

    leadCount = connection.query('SELECT COUNT() FROM Opportunity')
    newestLead = connection.query('SELECT Id, Name, Account.Name FROM Opportunity ORDER BY CreatedDate DESC LIMIT 1')
    print(leadCount['totalSize'])
    print(newestLead['records'][0]['Name'])
    args = anki_vector.util.parse_command_args()
    with anki_vector.Robot(args.serial) as robot:
        print("Say 'Hello World'...")
        robot.say_text("You have {0} Opportunities in Salesforce. Your newest opportunity is {1} for Account {2}.".format(leadCount['totalSize'], newestLead['records'][0]['Name'], newestLead['records'][0]['Account']['Name']))


if __name__ == "__main__":
    main()



