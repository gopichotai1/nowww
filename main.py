import random
import secrets
from flask import Flask, redirect , request , render_template, session, url_for , flash ,jsonify
import sqlite3
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask import flash
import os
from datetime import timedelta


app = Flask(__name__)

app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=5)

# Database setup
DATABASE = 'user.db'

# Allowed file extensions
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi'}
ALLOWED_EXTENSIONS_IMAGE = {'jpg', 'png', 'jfif'}

# Configure the upload folder
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
UPLOAD_FOLDER_IMAGE = 'static/upload'
app.config['UPLOAD_FOLDER_IMAGE'] = UPLOAD_FOLDER_IMAGE




# Check if the file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Initialize SQLite DB (if it doesn't exist)
# Check if the file is allowed
def allowed_file_IMAGE(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_IMAGE


        
@app.route('/like/<int:video_id>', methods=['POST'])
def like_video(video_id):
    user_email = session.get('email')

    if not user_email:
        return redirect(url_for('login'))  # Redirect to login if the user is not logged in

    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()

   
    # Update the likes count in the videos table
    cursor.execute('UPDATE videos SET likes = likes + 1 WHERE video_id = ?', (video_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('home'))

@app.route('/update_firstname',methods=['POST'])
def update_firstname():
    if 'email' in session:
        # Connect to the database
        conn = sqlite3.connect('user.db', timeout=100)
        conn.row_factory = sqlite3.Row  # This allows accessing columns by name
        reg_id=session.get('reg_id')
        cursor = conn.cursor()

        if request.method == 'POST':
            firstname = request.form['name']  
            # Update the user details in the database
            cursor.execute('UPDATE register_user SET firstname = ? WHERE reg_id = ?',(firstname,reg_id))
            conn.commit()
            # Close the database connection
            cursor.close()

            return redirect(url_for('account'))
        cursor.execute('SELECT * FROM users WHERE id = ?', (reg_id,))
        user = cursor.fetchone()
        conn.close()
        return render_template('account.html',user=user)
  
    return render_template('login.html')  

@app.route('/update_lastname',methods=['POST'])
def update_lastname():
    if 'email' in session:
        # Connect to the database
        conn = sqlite3.connect('user.db', timeout=100)
        conn.row_factory = sqlite3.Row  # This allows accessing columns by name
        reg_id=session.get('reg_id')
        cursor = conn.cursor()

        if request.method == 'POST':
            lastname = request.form['lastname']  
            # Update the user details in the database
            cursor.execute('UPDATE register_user SET lastname = ? WHERE reg_id = ?',(lastname,reg_id))
            conn.commit()
            # Close the database connection
            cursor.close()

            return redirect(url_for('account'))
        cursor.execute('SELECT * FROM users WHERE id = ?', (reg_id,))
        user = cursor.fetchone()
        conn.close()
        return render_template('account.html',user=user)
  
    return render_template('login.html')  

@app.route('/update_phone',methods=['POST'])
def update_phone():
    if 'email' in session:
        # Connect to the database
        conn = sqlite3.connect('user.db', timeout=100)
        conn.row_factory = sqlite3.Row  # This allows accessing columns by name
        reg_id=session.get('reg_id')
        cursor = conn.cursor()

        if request.method == 'POST':
            phone = request.form['phone']  
            # Update the user details in the database
            cursor.execute('UPDATE register_user SET phoneno = ? WHERE reg_id = ?',(phone,reg_id))
            conn.commit()
            # Close the database connection
            cursor.close()

            return redirect(url_for('account'))
        cursor.execute('SELECT * FROM users WHERE id = ?', (reg_id,))
        user = cursor.fetchone()
        conn.close()
        return render_template('account.html',user=user)
  
    return render_template('login.html')  



@app.route('/name')
def firstname():
    if 'email' in session:
        return render_template('firstname.html')
@app.route('/lastname')
def lastname():
    if 'email' in session:
        return render_template('lastname.html')

@app.route('/phonenumber')
def phonenumber():
    if 'email' in session:
        return render_template('phonenumber.html')


@app.route('/account')
def account():
    if 'email' in session:
        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()
        reg_id=session.get('reg_id')
        cursor.execute('SELECT profile_image FROM register_user WHERE reg_id=?',(reg_id,))
        images = cursor.fetchall()
        cursor.execute('SELECT reg_id,firstname,lastname,email,phoneno,age,gender,security_question,ans,date_time FROM register_user WHERE reg_id =?',(reg_id,))
        users=cursor.fetchall()
        return render_template('head.html',content='account.html', email=session['email'],users=users,images=images)
    return redirect(url_for('login'))

@app.route('/admin_account')
def admin_account():
    if 'email' in session:
        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()
        reg_id=session.get('reg_id')
        cursor.execute('SELECT reg_id,email FROM admin WHERE reg_id =?',(reg_id,))
        users=cursor.fetchall()
        return render_template('admin_head.html',content='admin_account.html', email=session['email'],users=users)
    return redirect(url_for('login'))


@app.route('/view_registration')
def view_registration():
    if 'email' in session:
        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()
        reg_id=session.get('reg_id')
        cursor.execute('SELECT * FROM register_user')
        users=cursor.fetchall()
        return render_template('admin_head.html',content='view_registration.html', email=session['email'],users=users)
    return redirect(url_for('login'))


@app.route('/view_all_video_details')
def view_all_video_details():
    if 'email' in session:
        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()
        reg_id=session.get('reg_id')
        cursor.execute('SELECT * FROM videos')
        users=cursor.fetchall()
        images = conn.execute('''
            SELECT register_user.profile_image,register_user.reg_id
            FROM register_user
            JOIN videos ON register_user.reg_id = videos.reg_id
            WHERE register_user.reg_id = videos.reg_id
            ''').fetchall()
        return render_template('admin_head.html',content='view_all_video_details.html', email=session['email'],users=users,images=images)
    return redirect(url_for('login'))

@app.route('/view_saved_video_details')
def view_saved_video_details():
    if 'email' in session:
        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()
        reg_id=session.get('reg_id')
        cursor.execute('SELECT * FROM videos')
        users=cursor.fetchall()
        return render_template('admin_head.html',content='view_all_video_details.html', email=session['email'],users=users)
    return redirect(url_for('login'))

@app.route('/history_video')
def history_video():
    conn = sqlite3.connect('user.db')        
    cursor = conn.cursor()
    reg_id=session.get('reg_id')

    # SQL Query to get all video watch history
    cursor.execute("SELECT * FROM video_history;")
    history = cursor.fetchall()

    conn.close()

    return render_template('history.html', history=history)

# Route to simulate watching a video and adding it to history
@app.route('/watch/<video_title>')
def watch_video(video_title):
    conn = sqlite3.connect('user.db')        
    cursor = conn.cursor()
    reg_id=session.get('reg_id')
    cursor = conn.cursor()

    # Simulate adding a video to the history
    watch_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO video_history (video_title, watch_time) VALUES (?, ?);", 
                   (video_title, watch_time))

    conn.commit()
    conn.close()
    return redirect(url_for('history'))

@app.route('/view_comment_details')
def view_comment_details():
    if 'email' in session:
        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()
        reg_id=session.get('reg_id')

        query='''
            SELECT register_user.email, videos.filename, comment.comment_text
            FROM register_user
            JOIN videos ON register_user.reg_id = comment.reg_id
            JOIN comment ON videos.video_id = comment.video_id
            '''

        rows = conn.execute(query).fetchall()

        

        return render_template('admin_head.html',content='view_comment_details.html', email=session['email'],rows=rows)
    return redirect(url_for('login'))


@app.route('/')
def hello():
    if 'email' in session:
        return render_template('head.html', email=session['email'])
    return redirect(url_for('login'))

@app.route('/admin_head')
def admin_head():
    if 'email' in session:
        return render_template('admin_head.html', email=session['email'])
    return redirect(url_for('login'))

@app.route('/view_liked_video')
def view_liked_video():
    if 'email' in session:
        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()
        
        reg_id = session.get('reg_id')
        cursor.execute("SELECT * FROM videos WHERE likes!='0'")
        videos = cursor.fetchall()
        conn.close()
    
    # Render the template and pass the necessary data
        return render_template('admin_head.html', content='view_liked_video.html',videos=videos,email=session['email'])
    return redirect(url_for('login'))

@app.route('/saved_videos')
def saved_videos():
    if 'email' in session:
        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()
        
        reg_id = session.get('reg_id')
        cursor.execute('''
            SELECT v.* 
            FROM videos v
            JOIN save_video sv ON v.video_id = sv.video_id
            WHERE sv.reg_id = ?
        ''', (reg_id,))
        images = conn.execute('''
            SELECT register_user.profile_image
            FROM register_user
            JOIN videos ON register_user.reg_id = videos.reg_id
            ''').fetchall()
        
        # Fetch all the resulting videos
        videos = cursor.fetchall()
        conn.close()
    
    # Render the template and pass the necessary data
        return render_template('head.html', content='saved_video.html',videos=videos,email=session['email'],images=images)
    return redirect(url_for('login'))


@app.route('/view_all_video')
def view_all_video():
    if 'email' in session:
        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()
        
        reg_id = session.get('reg_id')
        cursor.execute("SELECT * FROM videos")
        videos = cursor.fetchall()
        conn.close()
    
    # Render the template and pass the necessary data
        return render_template('admin_head.html', content='view_all_video.html',videos=videos,email=session['email'])
    return redirect(url_for('login'))

@app.route('/view_saved_videos')
def view_saved_videos():
    if 'email' in session:
        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()
        
        reg_id = session.get('reg_id')
        cursor.execute('''
            SELECT v.* 
            FROM videos v
            JOIN save_video sv ON v.video_id = sv.video_id
        ''')
        
        # Fetch all the resulting videos
        videos = cursor.fetchall()
        conn.close()
    
    # Render the template and pass the necessary data
        return render_template('admin_head.html', content='view_saved_video.html',videos=videos,email=session['email'])
    return redirect(url_for('login'))



@app.route('/shorts_video')
def shorts_video():
    if 'email' in session:
        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()
        images = conn.execute('''
            SELECT register_user.profile_image,register_user.reg_id
            FROM register_user
            JOIN videos ON register_user.reg_id = videos.reg_id
            WHERE register_user.reg_id = videos.reg_id
            ''').fetchall()
        reg_id = session.get('reg_id')
        cursor.execute("SELECT * FROM videos WHERE category='shorts'")
        videos = cursor.fetchall()
        conn.close()
    
    # Render the template and pass the necessary data
        return render_template('head.html', content='shorts.html',videos=videos,email=session['email'],images=images)
    return redirect(url_for('login'))

@app.route('/admin_shorts_video')
def admin_shorts_video():
    if 'email' in session:
        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()
        
        reg_id = session.get('reg_id')
        cursor.execute("SELECT * FROM videos WHERE category='shorts'")
        videos = cursor.fetchall()
        conn.close()
    
    # Render the template and pass the necessary data
        return render_template('admin_head.html', content='shorts.html',videos=videos,email=session['email'])
    return redirect(url_for('login'))


@app.route('/delete_video/<int:video_id>', methods=['POST'])
def delete_video(video_id):
    if 'email' in session:
        conn = sqlite3.connect('user.db' , timeout=100)
        conn.row_factory = sqlite3.Row  # This allows accessing columns by name

        cursor = conn.cursor()
        reg_id = session.get('reg_id')
        cursor.execute('DELETE FROM videos WHERE video_id=?',(video_id,))
        cursor.execute('SELECT * FROM videos WHERE reg_id=?',(reg_id,))        
        videos = cursor.fetchall()

        conn.commit()
        
        conn.close()
    
    # Render the template and pass the necessary data
        return render_template('head.html', content='your_video.html',email=session['email'],videos=videos)
    return redirect(url_for('login'))



@app.route('/delete_admin_video/<int:video_id>', methods=['POST'])
def delete_admin_video(video_id):
    if 'email' in session:
        conn = sqlite3.connect('user.db' , timeout=100)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM videos WHERE video_id=?',(video_id,))
        conn.commit()
        cursor.execute("SELECT * FROM videos")
        videos = cursor.fetchall()

        conn.close()
    
    # Render the template and pass the necessary data
        return render_template('admin_head.html', content='view_all_video.html',email=session['email'],videos=videos)
    return redirect(url_for('login'))


@app.route('/changes_password', methods=['GET', 'POST'] )
def changes_password():
    if 'email' in session:
        conn = sqlite3.connect('user.db' , timeout=100)
        cursor = conn.cursor()
        conn.row_factory = sqlite3.Row 
        currentPassword=request.form['currentPassword']
        newPassword=request.form['newPassword']
        confirmPassword=request.form['confirmPassword']

        if newPassword != confirmPassword:
            return render_template('change_password.html', error='New passwords and Confirm password are not match!')
        
        reg_id = session.get('reg_id')
        
        query = 'SELECT * FROM register_user WHERE reg_id = ?'
        user = conn.execute(query, (reg_id,)).fetchone()
        if user is None:
            flash("User not found!", "error")
            conn.close()
            return redirect(url_for('change_password'))
        
        if user['password'] != currentPassword:
            conn.close()
            return render_template('change_password.html', err='Incorrect current password!')
        if user['password'] == newPassword:
            conn.close()
            return render_template('change_password.html', er='Current password and New password are same!')
        cursor.execute('UPDATE register_user SET password=? WHERE reg_id=?',(newPassword,reg_id))
        conn.commit()
        
        conn.close()
    
    
        return render_template('head.html',email=session['email'])
    return redirect(url_for('login'))

@app.route('/forgotu', methods=['GET', 'POST'] )
def forgotu():
    
        conn = sqlite3.connect('user.db' , timeout=100)
        cursor = conn.cursor()
        conn.row_factory = sqlite3.Row 
        Username=request.form['Username']
        reg_id = session.get('reg_id')
        
        query = 'SELECT * FROM register_user WHERE email = ?'
        user = conn.execute(query, (Username,)).fetchone()
        if user is None:
            flash("User not found!", "error")
            conn.close()
            return render_template('register.html')
        if user['email'] != Username:
            conn.close()
            return render_template('forgotpass_1.html', err='Incorrect Username or email!')
        else:
            otp = ''.join([str(secrets.randbelow(10)) for _ in range(6)])

            return render_template('forgotpass_2.html',otp=otp)
        
    
@app.route('/forgotsa', methods=['GET', 'POST'] )
def forgotsa():
    
        conn = sqlite3.connect('user.db' , timeout=100)
        cursor = conn.cursor()
        conn.row_factory = sqlite3.Row

    
        # Pass the generated password to the template
        return render_template('forgotpass_3.html')

                    
        return render_template('forgotpass_3.html')
        

@app.route('/forgotp', methods=['GET', 'POST'] )
def forgotp():
    
        conn = sqlite3.connect('user.db' , timeout=100)
        cursor = conn.cursor()
        conn.row_factory = sqlite3.Row

        new_password=request.form['new_password']
        confirm_password=request.form['confirm_password']
        
        reg_id = session.get('reg_id')
        
        query = 'SELECT * FROM register_user WHERE email = ?'
        user = conn.execute(query, (Username,)).fetchone()
        if user is None:
            flash("User not found!", "error")
            conn.close()
            return redirect(url_for('change_password'))
        if new_password == confirm_password:
            conn.close()
            
            cursor.execute('UPDATE register_user SET password=? WHERE reg_id=?',(new_password,reg_id))
            conn.commit()
        
            conn.close()
        else:
            return render_template('change_password.html', er='New password and Confirm password are not same!')
    
    
        return render_template('head.html',email=session['email'])


    
@app.route('/home')
def home():
    if 'email' in session:

        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()
        reg_id=session.get('reg_id')
        cursor.execute('SELECT * FROM videos ORDER BY upload_time DESC')
        videos = cursor.fetchall()
        
        # Fetch videos and their like count
        cursor.execute('SELECT * FROM videos')
        videos = cursor.fetchall()
        images = conn.execute('''
            SELECT register_user.profile_image,register_user.reg_id
            FROM register_user
            JOIN videos ON register_user.reg_id = videos.reg_id
            WHERE register_user.reg_id = videos.reg_id
            ''').fetchall()
        
    
        return render_template('head.html', content='home.html', videos=videos,email=session['email'],images=images)
    return redirect(url_for('login'))

@app.route('/admin_home')
def admin_home():
    if 'email' in session:

        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM videos ORDER BY upload_time DESC')
        videos = cursor.fetchall()
        
        # Fetch videos and their like count
        cursor.execute('SELECT * FROM videos')
        videos = cursor.fetchall()

    
        return render_template('admin_head.html', content='home.html', videos=videos,email=session['email'])
    return redirect(url_for('login'))


@app.route('/history')
def history():
    if 'email' in session:
        return render_template('head.html', content='history.html',email=session['email'])

@app.route('/search', methods=['POST'])
def search():
    if 'email' in session:
        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()
        stextbox = request.form['stextbox']

        reg_id = session.get('reg_id')
        cursor.execute("SELECT * FROM videos WHERE category=? OR filename=? OR username=? ",(stextbox,stextbox,stextbox))
        videos = cursor.fetchall()
        rows = conn.execute('''
            SELECT videos.*
            FROM videos
            JOIN register_user ON videos.reg_id = register_user.reg_id
            WHERE register_user.email=?
            ''',(stextbox,)).fetchall()
        images = conn.execute('''
            SELECT register_user.profile_image,register_user.reg_id
            FROM register_user
            JOIN videos ON register_user.reg_id = videos.reg_id
            WHERE register_user.reg_id = videos.reg_id
            ''').fetchall()
        conn.close()
    # Render the template and pass the necessary data
        return render_template('head.html', content='home.html',videos=videos,email=session['email'],rows=rows,images=images)
    return redirect(url_for('login'))



@app.route('/your_video')
def your_video():
    if 'email' in session:
        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()
        reg_id = session.get('reg_id')
        cursor.execute("SELECT * FROM videos WHERE reg_id=?",(reg_id,))
        videos = cursor.fetchall()
        conn.close()    
        return render_template('head.html', content='your_video.html',videos=videos,email=session['email'])
    return redirect(url_for('login'))


@app.route('/liked_videos')
def liked_videos():
    if 'email' in session:
        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()
        stextbox = request.form['stextbox']

        reg_id = session.get('reg_id')
        cursor.execute("SELECT * FROM videos WHERE reg_id=? AND likes=?",(reg_id,))
        videos = cursor.fetchall()
        conn.close()
    
    # Render the template and pass the necessary data
        return render_template('head.html', content='home.html',videos=videos,email=session['email'])
    return redirect(url_for('login'))





@app.route('/comment/<int:video_id>', methods=['GET', 'POST'])
def comment(video_id):
    if 'email' in session:
        conn = sqlite3.connect('user.db', timeout=50.0)
        cursor = conn.cursor()
        conn.row_factory = sqlite3.Row  
        reg_id = session.get('reg_id')
        comment_text = request.form['textbox']

        cursor.execute("SELECT filename FROM videos WHERE video_id = ?", (video_id,))
        video = cursor.fetchone()

        # Fixed SQL query for inserting a new comment
        cursor.execute('''INSERT INTO comment ( reg_id, video_id, comment_text) 
                      VALUES (?, ?, ?)''', ( reg_id, video_id, comment_text))
        cursor.execute("SELECT comment_text FROM comment WHERE video_id = ?", (video_id,))
        comment = cursor.fetchall()
    
        conn.commit()  # Commit the transaction to save the data
        conn.close()
    
    # Render the template and pass the necessary data
        return render_template('head.html', content='home.html',email=session['email'],comment=comment)
    return redirect(url_for('login'))

@app.route('/save/<int:video_id>', methods=['GET', 'POST'])
def save(video_id):
    if 'email' in session:
        conn = sqlite3.connect('user.db', timeout=50.0)
        cursor = conn.cursor()
        conn.row_factory = sqlite3.Row  
        reg_id = session.get('reg_id')
        # Fixed SQL query for inserting a new comment
        cursor.execute('''INSERT INTO save_video ( reg_id, video_id) 
                      VALUES (?, ?)''', ( reg_id, video_id))
        
        conn.commit()  # Commit the transaction to save the data
        conn.close()
    
    # Render the template and pass the necessary data
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/comment_show', methods=['GET', 'POST'])
def comment_show():
    if 'email' in session:
        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()
        reg_id=session.get('reg_id')
        rows = conn.execute('''
            SELECT register_user.email, videos.filename, comment.comment_text
            FROM register_user
            JOIN videos ON register_user.reg_id = comment.reg_id
            JOIN comment ON videos.video_id = comment.video_id
            WHERE videos.reg_id=?
            ''',(reg_id,)).fetchall()

        return render_template('head.html', content='comment_show.html',email=session['email'],rows=rows)
    return redirect(url_for('login'))
    


@app.route('/youraccount')
def youraccount():
    if 'email' in session:
        return render_template('head.html', content='youraccount.html',email=session['email'])
    return redirect(url_for('login'))

'''@app.route('/contact')
def contact():
    return render_template('head.html', content='contact.html')'''

@app.route('/edit_profile')
def edit_profile():
    return render_template('head.html', content='edit_profile.html',email=session['email'])


@app.route('/liked_video')
def liked_video():
    if 'email' in session:
        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()
    
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM videos WHERE likes!=0")
            videos = cursor.fetchall()
            images = conn.execute('''
            SELECT register_user.profile_image
            FROM register_user
            JOIN videos ON register_user.reg_id = videos.reg_id
            ''').fetchall()
        return render_template('head.html', content='liked_video.html', videos=videos,email=session['email'],images=images)

   
    return render_template('head.html', content='liked_video.html')

@app.route('/video_upload', methods=['GET', 'POST'])
def video_upload():
    if 'email' in session:
        if request.method == 'POST':
        # Get file and user data
            file = request.files['file']
            username = request.form['username']
            category = request.form['category']
            reg_id = session.get('reg_id')
            conn = sqlite3.connect('user.db')
            cursor = conn.cursor()
            query = 'SELECT * FROM register_user WHERE reg_id = ?'
            user = conn.execute(query, (reg_id,)).fetchone()
           
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                reg_id=session.get('reg_id')
                # Save data to SQLite DB
                upload_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                with sqlite3.connect(DATABASE) as conn:
                    conn.execute('''INSERT INTO videos (filename, upload_time, username,category,likes,reg_id)
                                VALUES (?, ?, ? ,?,0,? )''', (filename, upload_time, username ,category,reg_id ))
                    conn.commit()
            
                return redirect(url_for('home'))
    
        return render_template('head.html', content='video_upload.html',email=session['email'])


@app.route('/image_upload', methods=['GET', 'POST'])
def image_upload():
    if 'email' in session:
        if request.method == 'POST':
        # Get file and user data  
            file = request.files['file']
            reg_id = session.get('reg_id')
            conn = sqlite3.connect('user.db')
            cursor = conn.cursor()
            query = 'SELECT * FROM register_user WHERE reg_id = ?'
            user = conn.execute(query, (reg_id,)).fetchone()
           
            if file and allowed_file_IMAGE(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER_IMAGE'], filename)
                file.save(filepath)
                reg_id=session.get('reg_id')
                # Save data to SQLite DB
                upload_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                with sqlite3.connect(DATABASE) as conn:
                    conn.execute('UPDATE register_user SET profile_image=? WHERE reg_id=?',(filename,reg_id))
                            
                    conn.commit()
            
                return redirect(url_for('show_profile'))
    
        return render_template('head.html', content='profile_image.html',email=session['email'])
    
@app.route('/show_profile')
def show_profile():
    if 'email' in session:

        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()
        reg_id=session.get('reg_id')
        cursor.execute('SELECT profile_image FROM register_user WHERE reg_id=?',(reg_id,))
        images = cursor.fetchall()

        return render_template('head.html', content='profile_img.html', images=images,email=session['email'])
    return redirect(url_for('login'))



@app.route('/saved_video')
def saved_video():
    return render_template('head.html', content='saved_video.html')


@app.route('/register')
def register():    
    # Data to populate the dropdown list
    dropdown_options = ['Option 1', 'Option 2', 'Option 3', 'Option 4']
    return render_template('register.html', options=dropdown_options)

@app.route('/change_password')
def change_password():
    return render_template('change_password.html')

@app.route('/forgot_password')
def forgot_password():
    return render_template('forgotpass_1.html')

@app.route('/forgotpass_2')
def forgotpass_2():
    return render_template('forgotpass_2.html')

@app.route('/forgotpass_3')
def forgotpass_3():
    return render_template('forgotpass_3.html')


    


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        phoneno = request.form['phoneno']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        hashed_password = generate_password_hash(password)
        hashed_password_confirm = generate_password_hash(confirm_password)
        age = request.form['age']
        gender = request.form['gender']
        security_question = request.form['security_question']
        ans = request.form['ans']
        date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        
        # Check if username already exists
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        c.execute('SELECT * FROM register_user WHERE email=?', (email,))
        existing_user = c.fetchone()

        if existing_user:
            
            return render_template('register.html', errors='Username already exists!')
            
        
        # Insert data into SQLite database
        conn = sqlite3.connect('user.db', timeout=50.0)
        c = conn.cursor()
        if password == confirm_password:
            c.execute('''
            INSERT INTO register_user (firstname, lastname, email, phoneno, password, age, gender, security_question, ans, date_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (firstname, lastname, email, phoneno, password, age, gender, security_question, ans, date_time))
            conn.commit()
            conn.close()
        else:
            return render_template('register.html', error='password not matched')

        flash("User registered successfully!", 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

# Route for User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Check if user exists and password is correct
        conn = sqlite3.connect('user.db', timeout=50.0)
        c = conn.cursor()
        c.execute('SELECT * FROM register_user WHERE email=? AND password=?', (email,password))
        
        user = c.fetchone()
        conn.close()
        conn = sqlite3.connect('user.db', timeout=50.0)
        con = conn.cursor()
    
        con.execute('SELECT * FROM admin WHERE email=? AND password=?', (email,password))
        users = con.fetchone()
        conn.close()    
        if users:
            session['reg_id'] = users[0]
            session['email'] = users[1]

            session.permanent = True # Store username in session
            return redirect(url_for('admin_head'))
        
        elif user:  # Compare hashed password
            session['reg_id'] = user[0]
            session['email'] = user[1]
            session['firstname'] = user[2]
            session['lastname'] = user[3]
            session['age'] = user[4]
            session['gender'] = user[5]
            session['security_question']=user[6]
            session['ans'] = user[7]
            session.permanent = True # Store username in session
            return redirect(url_for('hello'))
        else:
            return render_template('login.html', error='Invalid username or password')
            


    return render_template('login.html')

    
                            


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    
    app.run(debug=True)
    
