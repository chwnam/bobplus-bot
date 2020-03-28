import re
from urllib.request import urlopen
import json
from bs4 import BeautifulSoup


def get_html(url):
    return urlopen(url).read()


def test_grab():
    html = get_html('https://m.blog.naver.com/babplus123/221261990989')
    if html:
        with open('sample.html', 'wb') as f:
            f.write(html)


def get_bobplus_html():
    return get_html('https://m.blog.naver.com/babplus123/221261990989')
    

def parse_title(soup):
    return soup.find('h3', class_='tit_h3').get_text().strip()


def parse_menu(soup):
    r = re.compile(r'\s+')
    post_content = soup.find('div', class_='post_ct')
    content = post_content.find_all('p', recursive=False)
    menu_raw = '\n'.join([r.sub(' ', line) for line in map(lambda x: x.get_text(strip=True), content)])
    menu_raw = re.sub(r'\n{2,}', '\n', menu_raw, re.DOTALL | re.MULTILINE)
    menu_raw = menu_raw.replace('\ufeff', '')
    menu_raw = menu_raw.replace('\u200b', '')
    return menu_raw


def trim_menu(menu_raw):
    output = []
    r = re.compile(r'^([F0-9]{1,2})\s*:\s*(.+)$', re.MULTILINE)
    mk = None
    old_match = None

    for match in r.finditer(menu_raw):
        s = match.start(0)
        e = match.end(0)
        if mk:
            output.append(
                {
                    'code': old_match[1],
                    'branch': old_match[2],
                    'menu': menu_raw[mk:s].strip().split('\n')
                }
            )
        mk = e
        old_match = match

    return output


if __name__ == '__main__':
    soup = BeautifulSoup(get_bobplus_html(), 'html5lib')
    output = {
        'title': parse_title(soup),
        'data': trim_menu(parse_menu(soup))
    }
    print(json.dumps(output, indent=2, ensure_ascii=False))
