import json
import requests
import urllib3
import time

urllib3.disable_warnings()

headers = {'Content-Type': 'application/json'}
url = "https://localhost:9256/"
cert = ('ssl/full_node/private_full_node.crt', 'ssl/full_node/private_full_node.key')

## Constants
wallet_balance = "get_wallet_balance"
cat_spend = "cat_spend"

def submit(url, data, headers, cert):
    """needs to be submitted with url call"""
    response = json.loads(requests.post(url, data=data, headers=headers, cert=cert, verify=False).text)
    return(json.dumps(response, indent=4, sort_keys=True))

def get_wallet_balance(wallet_id):
    """shows the balance of all synced wallets"""
    data = '{"wallet_id": "%s"}'%wallet_id
    result = submit(url+wallet_balance,data,headers,cert)
    return json.loads(result)    

def spend_cat(address, wallet_id, spend_amount, fee):
    """send CAT transaction"""
    print("\n" + address)
    data = '{"wallet_id": %s, "amount": %s, "fee": %s, "inner_address": "%s"}'%(wallet_id,spend_amount,fee,address.strip())
    result = submit(url+cat_spend,data,headers,cert)
    return json.loads(result)

def spend_cat_list(list, wallet_id, spend_amount, fee):
    """sends cat to a list of addresses"""
    with open(list, "r") as f:
        for line in f:
            fail = True
            while fail:
                if get_wallet_balance(wallet_id)['wallet_balance']['spendable_balance'] and get_wallet_balance(1)['wallet_balance']['spendable_balance'] > 0:
                    spend = spend_cat(line, wallet_id, spend_amount, fee)
                    if spend['success'] == True:                    
                        print(spend)
                        fail = False
                    else:
                        fail = True
                        time.sleep(30)
                                               
if __name__ == "__main__":
    try:
        wallet_id = int((input("Input the wallet number you wish to send from: "))) #Wallet Number is based on number of CATS down in wallet
        print(f'\nReview and confirm this is the correct wallet: {get_wallet_balance(wallet_id)}')
        correct_wallet = input("Correct: Y/N? ").upper().strip()
        if correct_wallet == "Y":
            fee = int(input("\nEnter fee amount in Mojo: ").strip()) #in mojo
            spend_amount = int(input("\nEnter spend amount (1 x CAT Token = 1000): ").strip()) #1 whole CAT token is equal to 1000
            list_send = input("\nPlease confirm you have a file called list.txt with XCH addresses in the same folder as script (Y/N?): ").upper().strip()
            if list_send == "Y":
                confirm = input(f'\nWallet ID = {wallet_id} \nSpend amount = {spend_amount} \nFee = {fee}\nConfirm details are correct (Y/N?): ').upper().strip()
                if confirm == "Y":
                    spend_cat_list("list.txt", wallet_id, spend_amount, fee)
            else:
                print("CAT not sent")
    except ValueError:
        print("\nPlease enter Integer Value only when requested!")
                
    