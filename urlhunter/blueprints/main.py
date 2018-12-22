import requests
from more_itertools import flatten
from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app, Markup
from flask_login import login_required, current_user
from urlhunter.forms import URLForm, RegexForm
from urlhunter.utils import links
from urlhunter.models import Url, Regex
from urlhunter.extensions import db

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('main/index.html')


@bp.route('/extract', methods=['GET', 'POST'])
@login_required
def extract():
    form = URLForm()
    extracted_urls = None
    if form.validate_on_submit():
        try:
            if Url.query.count() > current_app.config['URL_LIMIT']:
                raise Exception(f"URL超限了！请先清空！[{Url.query.count()}/{current_app.config['URL_LIMIT']}]")
            urls = form.urls.data.split('\n')
            headers = {
                'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
            }
            responses = [
                requests.get(url.strip(), headers=headers) for url in urls
            ]
            if form.search.data:
                if form.use_regex.data is True:
                    extracted_urls = [
                        links(resp, pattern=form.search.data)
                        for resp in responses
                    ]
                else:
                    extracted_urls = [
                        links(resp, search=form.search.data)
                        for resp in responses
                    ]
            else:
                extracted_urls = [links(resp) for resp in responses]
            extracted_urls = list(flatten(extracted_urls))
            if len(extracted_urls) == 0:
                raise Exception('啊嘞？啥都没捕捉到哦U_U')
        except Exception as e:
            flash(e, 'danger')
        else:
            flash(
                Markup(
                    f"成功捕获到{len(extracted_urls)}条url XD <a href={url_for('main.show_urls')}>立即查看</a>"
                ), 'success')
            for extracted_url in extracted_urls:
                if not Url.query.filter_by(body=extracted_url).first():
                    url = Url(
                        body=extracted_url,
                        owner=current_user._get_current_object())
                    db.session.add(url)
            db.session.commit()
            return redirect(url_for('main.extract'))
    form.urls.data = request.args.get('urls')
    form.search.data = request.args.get('search')
    form.use_regex.data = bool(request.args.get('use_regex'))
    return render_template(
        'main/extract.html', form=form, extracted_urls=extracted_urls)


@bp.route('/urls')
@login_required
def show_urls():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['URL_PER_PAGE']
    current_user_urls = Url.query.with_parent(current_user)
    pagination = current_user_urls.order_by(
        Url.timestamp.desc()).paginate(page, per_page)
    urls = pagination.items
    outputs = '\n'.join([url.body for url in current_user_urls.all()])
    exclude_strings = request.args.get('exclude')
    if exclude_strings:
        urls, outputs = exclude_urls(exclude_strings, urls, current_user_urls)
    return render_template('main/urls.html', urls=urls, pagination=pagination, outputs=outputs)


@bp.route('/urls/delete/all', methods=['POST'])
@login_required
def delete_urls():
    urls = Url.query.with_parent(current_user._get_current_object()).all()
    db.session.execute('delete from url')
    db.session.commit()
    flash('操作成功！', 'success')
    return redirect(url_for('main.show_urls'))


@bp.route('/urls/search')
@login_required
def search_urls():
    q = request.args.get('q', '')
    if q == '':
        flash('请输入要搜索的URL', 'warning')
        return redirect(url_for('main.show_urls'))
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['SEARCH_PER_PAGE']
    searched_urls = Url.query.with_parent(current_user).filter(Url.body.ilike(f'%{q}%'))
    pagination = searched_urls.paginate(page, per_page)
    results = pagination.items
    outputs = '\n'.join([url.body for url in searched_urls.all()])
    exclude_strings = request.args.get('exclude')
    if exclude_strings:
        results, outputs = exclude_urls(exclude_strings, results, searched_urls)
    return render_template('main/search.html', pagination=pagination, results=results, q=q, outputs=outputs)


@bp.route('/regexs')
@login_required
def show_regexs():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['REGEX_PER_PAGE']
    pagination = Regex.query.with_parent(current_user).paginate(page, per_page)
    regexs = pagination.items
    return render_template('main/regexs.html', regexs=regexs, pagination=pagination)


@bp.route('/regexs/upload', methods=['GET', 'POST'])
@login_required
def upload_regex():
    form = RegexForm()
    if form.validate_on_submit():
        name = form.name.data
        site = form.site.data
        body = form.body.data
        regex = Regex(name=name, site=site, body=body, author=current_user._get_current_object())
        db.session.add(regex)
        db.session.commit()
        flash('添加成功！', 'success')
        return redirect(url_for('main.show_regexs'))
    return render_template('main/upload.html', form=form)


@bp.route('/help')
def show_help():
    return render_template('main/help.html')


@bp.app_template_global()
def exclude_urls(exclude_strings, paginated_urls, all_urls):
    exclude_strings = exclude_strings.split(',')
    excluded_paginated_urls = [url for url in paginated_urls if not any(es in url.body for es in exclude_strings)]
    excluded_all_urls = [url for url in all_urls.all() if not any(es in url.body for es in exclude_strings)]
    excluded_outputs = '\n'.join([url.body for url in excluded_all_urls])
    return excluded_paginated_urls, excluded_outputs
