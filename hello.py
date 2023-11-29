from flask import Flask,render_template,request
import pandas as pd
from tabulate import tabulate

app = Flask(__name__)

def csv_handling():
    df=pd.read_csv('menu/menu.csv')
    return df
    
@app.route("/")
def hello_world():
    return render_template('main.html')

@app.route('/billing', methods=['GET','POST'])
def billing():
    f_name=request.form['first_name']
    l_name=request.form['last_name']
    company=request.form['company']
    phone=request.form['phone']

    try:
        if 'file' not in request.files:
            return render_template('bill.html')
        file=request.files['file']
        file.save('menu/menu.csv')
        df=csv_handling()
        return render_template('bill.html',data=[df,company])
    except:
         return render_template('bill.html')

@app.route('/print', methods=['GET','POST'])
def printfy():
    items=request.form['items']
    df=csv_handling()
    items_list=items.split(",")
    temp_list=[]
    item_price=[]
    dfs_to_concat = []
    result_df = pd.DataFrame()

    for i in items_list:
        temp_list.append(i.split('-'))

    count=0
    for i in temp_list:
        no=i[0]
        qty=i[1]
        temp_df=df.loc[df['no'] == int(no)]
        count=count+1
        temp_df['no']=count
        temp_df['qty']=qty  
        temp_df['item_total']=temp_df.iloc[:,2].values*int(qty)
        dfs_to_concat.append(temp_df)

    result_df = pd.concat(dfs_to_concat, ignore_index=False)
    total = sum(result_df['item_total'])
    total_row = pd.DataFrame({'no': '','qty':'', 'name':'', 'price': 'Total', 'item_total':[total]})
    dfs_to_concat.append(total_row)
    result_df = pd.concat(dfs_to_concat, ignore_index=False)
    
    table = tabulate(result_df, headers='keys', tablefmt='pretty', showindex=False)
    with open('output.txt', 'w') as f:
        f.write(table)
        f.close()
    return render_template('print.html',data=[result_df,total])

if __name__ == '__main__':
     app.run(debug=True)
