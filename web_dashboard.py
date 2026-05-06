"""Web dashboard for real-time crawler monitoring."""
from flask import Flask, render_template, jsonify, send_file
from data_ingestion import DataIngestion
from visualization import Visualization
import os
import logging

# Suppress Flask logs
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
db = DataIngestion()
viz = Visualization()

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/stats')
def get_stats():
    return jsonify(viz.get_stats(print_output=False))

@app.route('/api/pages')
def get_pages():
    pages = db.get_all()
    return jsonify([{
        'id': p.id,
        'url': p.url, 
        'title': p.title, 
        'text': p.text_content,
        'status_code': p.status_code,
        'depth': p.depth
    } for p in pages[-20:]])

@app.route('/api/page/<int:page_id>')
def get_page_detail(page_id):
    page = db.session.query(db.CrawledPage).filter_by(id=page_id).first()
    if page:
        return jsonify({
            'url': page.url,
            'title': page.title,
            'text': page.text_content,
            'status_code': page.status_code,
            'depth': page.depth
        })
    return jsonify({})

@app.route('/chart')
def get_chart():
    chart_path = 'data/depth_chart.png'
    if os.path.exists(chart_path):
        return send_file(chart_path, mimetype='image/png')
    return '', 404

def start_dashboard():
    app.run(host='localhost', port=5000, debug=False)
