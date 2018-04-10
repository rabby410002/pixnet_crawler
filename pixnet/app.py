#!/usr/bin/python3
from flask import Flask
from flask import render_template
from flask import jsonify
from flask import Markup
from py import datasetprofile
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components
import esutil
import jconfig2
import mysql.connector

app = Flask(__name__, static_url_path='')
@app.route('/')
def mainform():
#    return "Hello! :)"
    return render_template('dash.html')


@app.context_processor
def utility_processor():
    def execsql(sqlstmt):
        cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database) 
        cursor = cnx.cursor()
        cursor.execute(sqlstmt)
        result=None
        for (u) in cursor:
            result=u[0]
            break
        return result
    return dict(execsql=execsql)


@app.route('/test')
def hello():
    return render_template('c.html')


@app.route('/vis')
def vis():
    r=esutil.get_result()
#    return render_template('gexf.html',nodes=r[0],relations=r[1])
    return render_template('vis.html',nodes=r[0],relations=r[1])



@app.route('/simple')
def simpleLine():
    fig=figure(title="Sensor data")
    fig.line([1,2,3,4],[2,4,6,8])
    script,div=components(fig)
    return render_template('simpleline.html',div=div,script=script)

@app.route('/trigger/<cmd>')
def trigger(cmd):
    from py import trigger
    from flask import Flask,redirect
    trigger.call(cmd)
    return redirect('/dash')


@app.route('/index.html')
def idx():
    from flask import Flask,redirect
    return redirect('/dash')



@app.route('/t2')
def t2():
    import py.jtrend
    lst=py.jtrend.get_list()
    
    return render_template('test.html',parent_dict=lst)


@app.route('/btrend')
def btrend():
#    import py.jtrend
    return render_template('brandtrend.html')


@app.route('/tsgroup')
def btrend2():
#    import py.jtrend
    return render_template('tsgroup.html')


@app.route('/gtrend/<bid>')
def gtrend(bid):
    import py.jtrend
    return jsonify( py.jtrend.gtrend(bid) )
@app.route('/ctrend/<bid>')
def ctrend(bid):
    import py.jtrend
    return jsonify( py.jtrend.ctrend(bid) )

@app.route('/gtrend2/<bid>')
def gtrend2(bid):
    import py.jtrend
    return jsonify( py.jtrend.gtrend2(bid) )

@app.route('/gtrend3/<bid>')
def gtrend3(bid):
    import py.jtrend
    return jsonify( py.jtrend.gtrend3(bid) )


@app.route('/trend_pix_list')
def pixlist():
    import py.jtrend
    return jsonify( py.jtrend.trend_pix_list() )

@app.route('/trend_brand_list')
def trendblist():
    import py.jtrend
    return jsonify( py.jtrend.trend_brand_list() )

@app.route('/trend_brand_list2')
def trendblist2():
    import py.jtrend
    return jsonify( py.jtrend.trend_brand_list2() )





@app.route('/reviews')
def reviews():
    import py.jtrend
    lst=py.jtrend.get_list()
    comments=datasetprofile.get_comments()

    return render_template('reviews.html',comments=comments)


@app.route('/table')
def tbl():
    return render_template('table.html')

@app.route('/dash')
def dash():
    pf=datasetprofile.get_dataset_profile()
    cstatus=datasetprofile.get_crawler_status()
    comments=datasetprofile.get_comments()
    return render_template('dashboard.html',profile=pf,cstatus=cstatus,comments=comments)



@app.template_filter()
def myfunc(data):
    return Markup("<h1>H1</h1>")

@app.route('/dummy')
def dummy():
    return render_template('dummy.html',test=[{'name':'a'},{'name':'b'},{'name':'c'}])



@app.route('/myjs')
def summary():
    d = [{'a':'b','c':'d'}]
    return jsonify(d)
@app.route('/ctrend2/<bid>')
def ctrend2(bid):
    import py.jtrend
    return jsonify( py.jtrend.ctrend2(bid) )

@app.route('/pixnet_trends')
def pixnet_trends():
    
    return render_template('pixnet_trends.html')

@app.route('/pixnet_season/<bid>')
def pixnet_season(bid):
    import py.jtrend
    return jsonify( py.jtrend.pixnet_season(bid) )


@app.route('/prophet')
def prophet():
    
    return render_template('prophet_test.html')




if __name__ == '__main__':
    app.run( 
        host="0.0.0.0",
        port=int("9897")
    )
