
## **Deribit Arbitrage**

## Setup Deribit_Arbitrage

|Action|Command
| :-| :-
|Create a virtual environment| python -m venv .venv
|Install relevant libraries | pip install -r requirements.txt|
|Create a .env file and add it to the root | .env
|User needs Deribit credentials | https://www.deribit.com/register|
|Create json launch file| Open and Paste contents of launch_items.txt (ensure commas are correct)|
|register models in  deribit_arb_app\models.py | Models in list_of models.txt|
|Run Make Migrations|Run & debug -> dropdown Menu -> Make Migrations |
|If  No Migration Changes |Ensure migrations folder with blank __init__.py file in |
|Run Migrations|Run & debug -> dropdown menu -> Migrate (No Relational db needed) |


## Enviroment Variables

|Environment variable|value|
| :-| :-
|CLIENT_ID|
|CLIENT_SECRET|

## Disclaimer
This trading Execution repository was created as a proof of theory/concept and should not be utilized in a trading environment. The code in this repository is provided for educational purposes only, and it is the sole responsibility of the user to determine whether the code is suitable for their intended use. The author of this repository does not make any representation or warranty as to the accuracy, completeness, or reliability of the information & performance contained herein. The user should be aware that there are risks associated with trading and that trading decisions should only be made after careful consideration of all relevant factors. The author of this repository will not be held responsible for any losses that may result from the use of this code.

## Executive Summary
This Repository provides infrastructure to execute trading strategies on the Deribit Exchange. The infrastructure provided has the ability to execute Arbitrage strategies by subscribing to multiple instrument order books and opening and closing positions based upon specific spreads/relationships. The Author of this repository has purposefully removed all strategies from this code to prevent plagiarism. 





