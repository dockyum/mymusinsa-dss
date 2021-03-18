import sys
sys.path.append('..')
from flask import *
from flask_sqlalchemy import SQLAlchemy
from config import Config
from sqlalchemy import or_


app = Flask(__name__)
app.config.update(TEMPLATES_AUTO_RELOAD=True, DEBUG=True)
app.config.from_object(Config)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = Config.DATABASE_URL

mysql_db = SQLAlchemy(app)

class Item(mysql_db.Model):
    _id = mysql_db.Column(mysql_db.Integer, primary_key=True, nullable=False)
    item_id = mysql_db.Column(mysql_db.String, unique=True, nullable=False)
    title = mysql_db.Column(mysql_db.String)
    brand = mysql_db.Column(mysql_db.String)
    o_price = mysql_db.Column(mysql_db.String)
    s_price = mysql_db.Column(mysql_db.String)
    kw = mysql_db.Column(mysql_db.String)
    img_link = mysql_db.Column(mysql_db.String)
    link = mysql_db.Column(mysql_db.String)
    rdate = mysql_db.Column(mysql_db.TIMESTAMP, nullable=False)
    
class Size(mysql_db.Model):
    A = mysql_db.Column(mysql_db.String)
    A_0 = mysql_db.Column(mysql_db.String)
    A_1 = mysql_db.Column(mysql_db.String)
    A_2 = mysql_db.Column(mysql_db.String)
    A_3 = mysql_db.Column(mysql_db.String)
    A_4 = mysql_db.Column(mysql_db.String)
    A_5 = mysql_db.Column(mysql_db.String)
    B = mysql_db.Column(mysql_db.String)
    B_0 = mysql_db.Column(mysql_db.String)
    B_1 = mysql_db.Column(mysql_db.String)
    B_2 = mysql_db.Column(mysql_db.String)
    B_3 = mysql_db.Column(mysql_db.String)
    B_4 = mysql_db.Column(mysql_db.String)
    B_5 = mysql_db.Column(mysql_db.String)
    C = mysql_db.Column(mysql_db.String)
    C_0 = mysql_db.Column(mysql_db.String)
    C_1 = mysql_db.Column(mysql_db.String)
    C_2 = mysql_db.Column(mysql_db.String)
    C_3 = mysql_db.Column(mysql_db.String)
    C_4 = mysql_db.Column(mysql_db.String)
    C_5 = mysql_db.Column(mysql_db.String)
    D = mysql_db.Column(mysql_db.String)
    D_0 = mysql_db.Column(mysql_db.String)
    D_1 = mysql_db.Column(mysql_db.String)
    D_2 = mysql_db.Column(mysql_db.String)
    D_3 = mysql_db.Column(mysql_db.String)
    D_4 = mysql_db.Column(mysql_db.String)
    D_5 = mysql_db.Column(mysql_db.String)
    E = mysql_db.Column(mysql_db.String)
    E_0 = mysql_db.Column(mysql_db.String)
    E_1 = mysql_db.Column(mysql_db.String)
    E_2 = mysql_db.Column(mysql_db.String)
    E_3 = mysql_db.Column(mysql_db.String)
    E_4 = mysql_db.Column(mysql_db.String)
    E_5 = mysql_db.Column(mysql_db.String)
    F = mysql_db.Column(mysql_db.String)
    F_0 = mysql_db.Column(mysql_db.String)
    F_1 = mysql_db.Column(mysql_db.String)
    F_2 = mysql_db.Column(mysql_db.String)
    F_3 = mysql_db.Column(mysql_db.String)
    F_4 = mysql_db.Column(mysql_db.String)
    F_5 = mysql_db.Column(mysql_db.String)
    G = mysql_db.Column(mysql_db.String)
    G_0 = mysql_db.Column(mysql_db.String)
    G_1 = mysql_db.Column(mysql_db.String)
    G_2 = mysql_db.Column(mysql_db.String)
    G_3 = mysql_db.Column(mysql_db.String)
    G_4 = mysql_db.Column(mysql_db.String)
    G_5 = mysql_db.Column(mysql_db.String)
    _0 = mysql_db.Column(mysql_db.String)
    _1 = mysql_db.Column(mysql_db.String)
    _2 = mysql_db.Column(mysql_db.String)
    _3 = mysql_db.Column(mysql_db.String)
    _4 = mysql_db.Column(mysql_db.String)
    _5 = mysql_db.Column(mysql_db.String)
    item_id = mysql_db.Column(mysql_db.String, unique=True, nullable=False)
    main_code = mysql_db.Column(mysql_db.String)
    _id = mysql_db.Column(mysql_db.Integer, primary_key=True, nullable=False)
    
mysql_db.create_all()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/getdatas')
def get_datas():
    
    maincode = request.values.get("maincode")
    size_values = {}
    for num in range(1,5):
        if request.values.get(f"v{num}"):
        #             vals = int()
            size_values[f"v{num}"] = request.values.get(f"v{num}")
    #         [str(vals-1), str(vals), str(vals+1)]
        
    print(size_values)
    
    if maincode in ['001', '002', '020']:
        query_request = Size.query.filter(Size.main_code == maincode).filter(or_(Size.A_0 == size_values["v1"], Size.A_1 == size_values["v2"], Size.A_2 == size_values["v3"], Size.A_3 == size_values["v4"])).limit(10)
        rs = [result.item_id for result in query_request]
        query_request = Size.query.filter(Size.main_code == maincode).filter(or_(Size.B_0 == size_values["v1"], Size.B_1 == size_values["v2"], Size.B_2 == size_values["v3"], Size.B_3 == size_values["v4"])).limit(10)
        rs += [result.item_id for result in query_request]
        query_request = Size.query.filter(Size.main_code == maincode).filter(or_(Size.C_0 == size_values["v1"], Size.C_1 == size_values["v2"], Size.C_2 == size_values["v3"], Size.C_3 == size_values["v4"])).limit(10)
        rs += [result.item_id for result in query_request]
        query_request = Size.query.filter(Size.main_code == maincode).filter(or_(Size.D_0 == size_values["v1"], Size.D_1 == size_values["v2"], Size.D_2 == size_values["v3"], Size.D_3 == size_values["v4"])).limit(10)
        rs += [result.item_id for result in query_request]
        query_request = Size.query.filter(Size.main_code == maincode).filter(or_(Size.E_0 == size_values["v1"], Size.E_1 == size_values["v2"], Size.E_2 == size_values["v3"], Size.E_3 == size_values["v4"])).limit(10)
        rs += [result.item_id for result in query_request]
        query_request = Size.query.filter(Size.main_code == maincode).filter(or_(Size.F_0 == size_values["v1"], Size.F_1 == size_values["v2"], Size.D_2 == size_values["v3"], Size.D_3 == size_values["v4"])).limit(10)
        rs += [result.item_id for result in query_request]
        query_request = Size.query.filter(Size.main_code == maincode).filter(or_(Size.G_0 == size_values["v1"], Size.G_1 == size_values["v2"], Size.D_2 == size_values["v3"], Size.D_3 == size_values["v4"])).limit(10)
        rs += [result.item_id for result in query_request]
    elif maincode == '003':
        query_request = Size.query.filter(Size.main_code == maincode).filter(Size.A_0.in_(size_values["v1"])).filter(Size.A_1.in_(size_values["v2"])).filter(Size.A_2.in_(size_values["v3"])).filter(Size.A_3.in_(size_values["v4"])).filter(Size.A_4.in_(size_values["v5"])).limit(5)
        rs = [result.item_id for result in query_request]
    elif maincode == '022':
        query_request = Size.query.filter(Size.main_code == maincode).filter(Size.A_0.in_(size_values["v1"])).filter(Size.A_1.in_(size_values["v2"])).filter(Size.A_2.in_(size_values["v3"])).limit(5)
        rs = [result.item_id for result in query_request]
    
    items = Item.query.filter(Item.item_id.in_(rs))
    
    result = {}
    datas = []
    for item in items:
        datas.append({"title":item.title, "brand": item.brand, "url" : item.link, "img" : item.img_link})
    result['datas'] = datas
    return jsonify(result)
    
app.run(debug=True)
