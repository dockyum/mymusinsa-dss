from flask import *
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.update(TEMPLATES_AUTO_RELOAD=True, DEBUG=True)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:dss@3.36.125.234:3306/mymusinsa?charset=utf8"

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


@app.route('/get_datas')
def get_datas():
    search_results = Size.query.filter(Size.A_0 == "50", Size.A_1 == '43', Size.main_code == '002')
    rs = [result.item_id for result in search_results]
    items = Item.query.filter(Item.item_id.in_(rs))
    
    result = {}
    datas = []
    for item in items:
        datas.append({"title":item.title, "brand": item.brand})
    result['datas'] = datas
    return jsonify(result)
    
app.run(debug=True)
