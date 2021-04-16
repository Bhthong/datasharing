import os, json, random
from flask import Flask, render_template, url_for, flash, redirect
from forms import LoginForm, TransactionForm
import ipfshttpclient

UPLOAD_FOLDER = '/home/ndthuc/bhthong'

class IpfsMaster():
  ADDRESS_BASE = '/ip4/{0}/tcp/{1}/http'

  def __init__(self, config_path):
    self.__config = []
    config = None
    with open(config_path, 'r') as f:
      config = json.load(f)
    if type(config) is not list:
      return
    for node in config:
      if (type(node) is not dict) or ('ip' not in node) or ('port' not in node):
        continue
      self.__config.append({'ip': node['ip'], 'port': node['port']})

  def getClient(self):
    if len(self.__config) < 1:
      return None
    rand = random.randrange(len(self.__config))
    client = None
    for i in range(len(self.__config)):
      node = self.__config[(rand + i) % len(self.__config)]
      try:
        ip = node['ip']
        port = node['port']
        client = ipfshttpclient.connect(self.ADDRESS_BASE.format(ip, port))
        break
      except:
        client = None
        continue
    return client


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

@app.route("/")
def login1():
    return redirect(url_for('transaction'))


@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/transaction", methods=['GET', 'POST'])
def transaction():
    form = TransactionForm()
    if form.validate_on_submit():
        if form.file.data:
            ipfs_master = IpfsMaster("example.conf")
            client = ipfs_master.getClient()
            path = os.path.join(UPLOAD_FOLDER, form.file.data.filename)
            form.file.data.save(path)
            info = client.add(path)
            result = client.object.patch.add_link(info['Hash'], info['Name'], info['Hash'])
            hash_str = result['Hash']
            client.close()
            flash(hash_str)
            #return redirect("https://rinkeby.etherscan.io/tx/0x852ce8ca4875c0084635b7133a3b6d8e804bb61e22f9e0567b401f941c78a739?fbclid=IwAR0LsnLbqCNadLGqkeRvgdba5TeYXBmSE1h_UBeQzjar23Gfkt6nfN0Psj0")
        else:
            flash('Unsuccessful', 'danger')
    return render_template('trans.html', title='Transaction', form=form)

if __name__ == '__main__':
      app.run(debug = True, host = '0.0.0.0', port = 8000)