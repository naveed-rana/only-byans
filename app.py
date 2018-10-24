from flask import Flask,render_template,request,url_for,g,session,redirect,jsonify
import pafy,string,random,time
import MySQLdb as mys
import math
import os

con = mys.connect('myonlybyaninstance.cqftgg4dkoaz.us-east-1.rds.amazonaws.com','naveed5547','naveedrana','onlybayan')
c = con.cursor()
app = Flask(__name__)
app.secret_key = os.urandom(24)

#Function For Admin-panel
def identify_slug(slug):
    q = 'SELECT *FROM records WHERE SLUG = %s'
    value = (slug,)
    c.execute(q,value)
    res = c.fetchone()
    if res:
        choose = string.digits
        choose = ''.join(random.choice(choose) for i in range(random.randint(1,3)))
        choose = str(choose)
        slug = slug + '-' + choose
    return slug
    

def create_slug_postid_time(title):
    title = title.lower()
    slug = '-'.join(title.split(' '))
    slug = identify_slug(slug)
    postid = string.ascii_letters + string.digits
    while True:
        postid = ''.join(random.choice(postid) for i in range(random.randint(3,10)))
        q = 'SELECT *FROM records WHERE POSTID = %s'
        value = (postid,)
        c.execute(q,value)
        res = c.fetchone()
        if res:
            continue
        else:
            break
    
    current_time = time.strftime('%H:%M,%Y-%m-%d %p')
    return slug,postid,current_time


def upload_content(title,category,author,url,description,content):
    
    if title == '':
        video = pafy.new(url)
        title = video.title
    slug,postid,current_time = create_slug_postid_time(title)
    category = int(category)
    category_select = ''
    if category == 1:
        category_select = 'namaz'
    elif category == 2:
        category_select = 'success'
    elif category == 3:
        category_select = 'motivation'
    elif category == 4:
        category_select = 'azan'
    elif category == 5:
        category_select = 'status'
    elif category == 6:
        category_select = 'life-changing'
    
    fast_upload(title,slug,author,postid,category_select,url,description,content,current_time)



def fast_upload(title,slug,author,postid,category,url,description,content,current_time):
    q = 'INSERT INTO records(title,slug,author,postid,category,url,description,content,time) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    values = (title,slug,author,postid,category,url,description,content,current_time,)
    c.execute(q,values)
    con.commit()

#End function For Admin
#-------------------------


#User Function
"""
def get_data():
    q = "SELECT *FROM records WHERE CATEGORY = 'namaz'"
    c.execute(q)
    res = c.fetchall()
    return res

"""


def pagination_controler(page,category):
    try:
        if page !=0:
            if page == None:
                page = 1
            

            perpage = 12
            limit = 0
            if page > 1:
                limit = (page * perpage) - perpage
            q = "SELECT *FROM records WHERE CATEGORY= %s ORDER BY TIMESTAMP DESC LIMIT %s,%s"
            values = (category,limit,perpage)
            c.execute(q,values)
            records = c.fetchall()
            total = 0
            c.execute("select *from records where category = '{}'".format(category))
            counts = c.fetchall()
            for i in counts:
                total +=1
            pages = math.ceil(total/perpage)
            if pages < page:
                return False,False,False

            return records,pages,page
        return False,False,False
    
    except Exception as e:
        return False,False,False
    

def get_search_data(page,data):
    perpage = 9
    limit = 0
    if page > 1:
        limit = (page * perpage) - perpage
        
    q = "SELECT *FROM records WHERE TITLE LIKE '{}' ORDER BY TIMESTAMP DESC LIMIT {},{}".format('%'+data+'%',limit,perpage)

    c.execute(q)
    records = c.fetchall()
    total = 0
    c.execute("select *from records where title like '{}'".format('%'+data+'%'))
    counts = c.fetchall()
    for i in counts:
        total +=1
    pages = math.ceil(total/perpage)

    if pages < page:
        return False,False,False
    return records,pages,page


def get_home_data(category):
    q = 'SELECT *FROM records WHERE CATEGORY = %s ORDER BY TIMESTAMP DESC LIMIT 0,3'
    value = (category,)
    c.execute(q,value)
    res = c.fetchall()
    return res

#End user Function

#For User To show Anything
@app.route('/')
def index():
    namaz = get_home_data('namaz')
    success = get_home_data('success')
    motivation = get_home_data('motivation')
    azan = get_home_data('azan')
    status = get_home_data('status')
    life = get_home_data('life-changing')
    return render_template('index.html',namaz=namaz,success=success,motivation=motivation,azan=azan,status=status,life=life)


@app.route('/namaz/')
@app.route('/namaz/<int:page>')
def namaz(page=None):
    records,pages,page = pagination_controler(page,'namaz')
    if records:
        return render_template('namaz.html',res=records,pages = pages,page=page)
    return redirect(url_for('page_not_found'))

@app.route('/success/')
@app.route('/success/<int:page>')
def success(page=None):
    records,pages,page = pagination_controler(page,'success')
    if records:
        return render_template('success.html',res=records,pages = pages,page=page)
    return redirect(url_for('page_not_found'))

@app.route('/motivation/')
@app.route('/motivation/<int:page>')
def motivation(page=None):
    records,pages,page = pagination_controler(page,'motivation')
    if records:
        return render_template('motivation.html',res=records,pages = pages,page=page)
    return redirect(url_for('page_not_found'))
    

@app.route('/azan/')
@app.route('/azan/<int:page>')
def azan(page=None):
    records,pages,page = pagination_controler(page,'azan')
    if records:        
        return render_template('azan.html',res=records,pages = pages,page=page)
    return redirect(url_for('page_not_found'))

@app.route('/status/')
@app.route('/status/<int:page>')
def status(page=None):
    records,pages,page = pagination_controler(page,'status')
    if records:
        return render_template('status.html',res=records,pages = pages,page=page)
    return redirect(url_for('page_not_found'))

@app.route('/life-changing/')
@app.route('/life-changing/<int:page>')
def life(page=None):
    records,pages,page = pagination_controler(page,'life-changing')
    if records:        
        return render_template('life.html',res=records,pages = pages,page=page)
    return redirect(url_for('page_not_found'))


@app.route('/<string:category>/<string:slug>')
def preview(category,slug):
    try:
        q = 'SELECT *FROM records WHERE CATEGORY = %s AND SLUG = %s'
        values = (category,slug,)
        c.execute(q,values)
        res = c.fetchone()
        if res:
            related_q = 'SELECT * FROM records ORDER BY RAND() LIMIT 7'
            c.execute(related_q)
            related_data = c.fetchall()
            return render_template('preview.html',res = res,related = related_data)
        return redirect(url_for('page_not_found'))
    except Exception as e:
        return redirect((url_for('page_not_found')))

@app.route('/genrate_download_link',methods=['GET','POST'])
def genrate_download_link():
    if request.method == 'POST':
        url = request.form['url']
        video = pafy.new(url)

        return jsonify({'data':render_template('download_preview.html',url=url,video=video)})



@app.route('/<int:page>/search',methods= ['GET'])
def search_engine(page):
    try:

        if request.method == 'GET':
            search = request.args['q']
        if (search != '') and (page >=1):
            records,pages,page = get_search_data(page,search)
            return render_template('search.html',search=search,page=page,pages=pages,res = records)
        return redirect(url_for('index')) 
    except Exception as e:
        return redirect(url_for('page_not_found'))
    

#Admin Panel
@app.route('/admin-panel/admin/login-system')
def admin_login():
    if not g.admin:
        return render_template('admin-login.html')
    return redirect(url_for('admin_panel'))

@app.route('/admin-panel/admin/admin-system')
def admin_panel():
    if g.admin:
        return render_template('admin-panel.html')
    return redirect(url_for('admin_login'))

@app.route('/admin-panel/admin/admin-seeall')
def admin_seeall():
    if g.admin:
        q = 'SELECT *FROM records ORDER BY TIMESTAMP DESC'
        c.execute(q)
        data = c.fetchall()
        return render_template('admin-seeall.html',data=data)
    return redirect(url_for('admin_login'))

@app.route('/admin-panel/admin/admin-delete/<string:category>/<string:postid>')
def admin_delete(category,postid):
    if g.admin:
        try:
            q = 'DELETE FROM records WHERE CATEGORY = %s AND POSTID = %s'
            values = (category,postid,)
            c.execute(q,values)
            con.commit()
        except Exception as i:
            return i
        
        return redirect(url_for('admin_seeall'))
    
    return redirect(url_for('admin_login'))

#Admin UPload fetching
@app.route('/upload',methods=['GET','POST'])
def upload():
    if g.admin:
        if request.method == 'POST':
            
            title = request.form['title']
            category = request.form['category']
            author = request.form['author']
            url = request.form['url']
            description = request.form['description']
            content = request.form['content']
            if (author == '') or (url == '') or (description == ''):
                raise ValueError('Empty')
            
            upload_content(title,category,author,url,description,content)
            return jsonify({'success':'Uploading Completed'})
    return redirect(url_for('admin_login'))

#Admin login

@app.route('/authentication',methods = ['GET','POST'])
def authentication():
    try:

        if request.method == 'POST':
            admin_name = request.form['admin']
            admin_pass = request.form['password']
            session.pop('admin',None)
            if (admin_name == 'pakamnan786') and (admin_pass == 'Pakamnan786@@'):
                session['admin'] = admin_name
                return redirect(url_for('admin_panel'))
            return 'Incrorect password or username'
        return redirect(url_for('page_not_found'))    
    except Exception as e:
        return e


@app.before_request
def before_request():
    g.admin = None
    if 'admin' in session:
        g.admin = session['admin']

#End login

@app.errorhandler(404)
@app.route('/page-not-found')
def page_not_found(e=None):
    return render_template('404.html')

@app.errorhandler(403)
def error_403(e):
    return 'sorry'

@app.errorhandler(410)
def error_410(e):
    return 'sorry'

@app.errorhandler(400)
def error_400(e):
    return 'sorry'

@app.errorhandler(500)
def error_500(e):
    return 'sorry'

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(port)
    app.run(host='0.0.0.0', port=port)




