from flask import render_template, redirect, url_for, session, flash, abort
from database import app, Review, User, db
from forms import RegistrationForm, LoginForm, ReviewForm


@app.route('/')
def home():
    reviews = Review.query.all()
    return render_template('index.html', reviews=reviews)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    message = None
    if form.validate_on_submit():
        user = User(login=form.login.data)
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        message = 'Ваш аккаунт создан! Теперь можете войти.'
    return render_template('register.html', form=form, message=message)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()
        if (user and user.password == form.password.data):
            session['user_id'] = user.id
            return redirect(url_for('profile'))
        else:
            flash('Неправильный логин или пароль.', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html', form=form)



@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    return render_template('profile.html', reviews=user.reviews)

@app.route('/create_review', methods=['GET', 'POST'])
def create_review():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(
            movie_title=form.movie_title.data,
            rating=form.rating.data,
            review_text=form.review_text.data,
            image_url=form.image_url.data,
            user_id=session['user_id']
        )
        db.session.add(review)
        db.session.commit()
        flash('Ваш отзыв был успешно создан!', 'success')
        return redirect(url_for('home'))

    return render_template('create_review.html', form=form)

@app.route('/review/<int:review_id>')
def review_detail(review_id):
    review = Review.query.get(review_id)
    if review is None:
        abort(404)
    return render_template('review_detail.html', review=review)


@app.route('/edit_review/<int:review_id>', methods=['GET', 'POST'])
def edit_review(review_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    review = Review.query.get(review_id)
    if review is None or review.user_id != session['user_id']:
        abort(404)

    form = ReviewForm(obj=review)
    if form.validate_on_submit():
        review.movie_title = form.movie_title.data
        review.rating = form.rating.data
        review.review_text = form.review_text.data
        review.image_url = form.image_url.data
        db.session.commit()
        flash('Ваш отзыв был успешно обновлён!', 'success')
        return redirect(url_for('profile'))

    return render_template('edit_review.html', form=form, review=review)

@app.route('/delete_review/<int:review_id>', methods=['POST'])
def delete_review(review_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    review = Review.query.get(review_id)
    if review is None or review.user_id != session['user_id']:
        abort(404)

    db.session.delete(review)
    db.session.commit()
    flash('Ваш отзыв был успешно удалён!', 'success')
    return redirect(url_for('profile'))

if __name__ == '__main__':
    app.run()