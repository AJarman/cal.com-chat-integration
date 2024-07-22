import datetime as dt


from pydantic import BaseModel, Field
from langchain_core.tools import tool
import requests

from cal import CAL_API_KEY, CAL_USERNAME, CAL_USER_ID

CHECK_ENDPOINT = "https://api.cal.com/v1/availability"
TODAY:dt.date = dt.date.today()
ONE_WEEK_FUTURE:dt.date = TODAY + dt.timedelta(days=7)

class GetAvailiablityInput(BaseModel):
    event_type_id: str = Field(..., description="The event type id to check availiability for")
    cal_api_key: str = Field(CAL_API_KEY, description="The cal.com api key")
    cal_user_id: str = Field(CAL_USER_ID, description="The event type id to check availiability for")
    cal_username: str = Field(CAL_USERNAME, description="The event type id to check availiability for")
    date_from: dt.datetime = Field(TODAY, description="The start date to check availiability in the calendar, inclusive")
    date_to: dt.datetime = Field(ONE_WEEK_FUTURE, description="The start date to check availiability in the calendar, inclusive")

@tool("check_cal_availiability",args_schema=GetAvailiablityInput, description="Check availiability for a given event type", return_direct=True)
def check_availiability(
                        event_type_id:str,
                        date_from:dt.date=TODAY, 
                        date_to:dt.date=ONE_WEEK_FUTURE, 
                        cal_api_key:str=CAL_API_KEY,
                        cal_username:str=CAL_USERNAME, 
                        cal_user_id:str=CAL_USER_ID):
    """
    Query

    apiKey	Your API key
    userId	ID of the user to fetch the availability for
    username	username of the user to fetch the availability for
    dateFrom	Start Date of the availability query
    dateTo	End Date of the availability query
    eventTypeId	Event Type ID of the event type to fetch the availability for.
    """
    
    params  = {
        "apiKey": cal_api_key,
        "userId": cal_user_id,
        "username": cal_username,
        "dateFrom": date_from,
        "dateTo": date_to,
        "eventTypeId": event_type_id
    }
    response = requests.get(CHECK_ENDPOINT, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Failed to get availiability for event type {event_type_id}")
    else:
        return response.json()
    
    
if __name__ == "__main__":
    print(check_availiability("30m", date_to=ONE_WEEK_FUTURE+dt.timedelta(days=9)))

