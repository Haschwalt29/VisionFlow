"""
VisionFlow Flask Backend
AI Workflow Automation Agent - Data Extraction API
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from database import init_db, add_extraction, get_recent_extractions, close_connection
from extract import process_url

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Initialize database
init_db()

@app.teardown_appcontext
def close_db(error):
    """Close database connection when app context is torn down"""
    from flask import g
    close_connection(error)

@app.route('/', methods=['get'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "VisionFlow API",
        "version": "1.0.0"
    })

@app.route('/extract', methods=['POST'])
def extract_data():
    """Extract structured data from a webpage URL"""
    try:
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({
                "success": False,
                "error": "URL is required"
            }), 400
        
        url = data['url'].strip()
        
        # Basic URL validation
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Process the URL
        result = process_url(url)
        
        if result['success']:
            # Store in database
            extraction_id = add_extraction(
                url=url,
                extracted_data=result['data'],
                raw_html="",  # We're not storing raw HTML to save space
                status="success"
            )
            
            return jsonify({
                "success": True,
                "extraction_id": extraction_id,
                "data": result['data'],
                "url": url,
                "message": "Data extracted successfully"
            })
        else:
            # Store failed extraction
            add_extraction(
                url=url,
                extracted_data={},
                raw_html="",
                status="failed"
            )
            
            return jsonify({
                "success": False,
                "error": result['error']
            }), 500
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Server error: {str(e)}"
        }), 500

@app.route('/data', methods=['GET'])
def get_data():
    """Get recent extractions from database"""
    try:
        limit = request.args.get('limit', 50, type=int)
        extractions = get_recent_extractions(limit)
        
        return jsonify({
            "success": True,
            "data": extractions,
            "count": len(extractions)
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Database error: {str(e)}"
        }), 500

@app.route('/extractions/<int:extraction_id>', methods=['GET'])
def get_extraction(extraction_id):
    """Get a specific extraction by ID"""
    try:
        from database import get_db
        
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('''
            SELECT id, url, name, description, features, pricing, extracted_at, status
            FROM extractions
            WHERE id = ?
        ''', (extraction_id,))
        
        row = cursor.fetchone()
        
        if row:
            extraction = {
                'id': row[0],
                'url': row[1],
                'name': row[2],
                'description': row[3],
                'features': row[4],
                'pricing': row[5],
                'extracted_at': row[6],
                'status': row[7]
            }
            
            return jsonify({
                "success": True,
                "data": extraction
            })
        else:
            return jsonify({
                "success": False,
                "error": "Extraction not found"
            }), 404
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Database error: {str(e)}"
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"success": False, "error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"success": False, "error": "Internal server error"}), 500

if __name__ == '__main__':
    # Check if Google AI API key is set
    if not os.getenv('GOOGLE_AI_API_KEY'):
        print("⚠️  WARNING: GOOGLE_AI_API_KEY not found in environment variables")
        print("Please create a .env file and add your Google AI API key:")
        print("GOOGLE_AI_API_KEY=your_google_ai_api_key_here")
    
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"🚀 Starting VisionFlow API on port {port}")
    print(f"📊 Database initialized")
    print(f"🤖 Gemini AI integration ready")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
