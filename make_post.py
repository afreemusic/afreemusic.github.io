import os
import random
import glob
from datetime import datetime

songs_dir = '/Users/longhengyu/Dropbox/misc/梅路卡里/long/ai-music/已选曲'

post_template = '''---
title: %s
date: %s
cover_image: ./post_covers/%s.jpg
---
%s

<div class="video-container">
    <iframe width="1920" height="1080" src="https://www.youtube.com/embed/%s" frameborder="0" allowfullscreen>
    </iframe>
</div>
<br>

Download the Audio Track: [https://hexo.io/docs/writing.html](https://hexo.io/docs/writing.html)

'''


def get_meta(path):
    meta = {}
    try:
        meta_file = glob.glob(path + '/meta.txt')[0]
        with open(meta_file, 'r') as f:
            meta['title'] = f.readline().strip()
            meta['tags'] = f.readline().strip()
            meta['template'] = f.readline().strip()
            meta['ytid'] = f.readline().strip()
    except:
        pass
    return meta


if __name__ == "__main__":

    songs = [s for s in glob.glob(songs_dir + '/*') if '.DS_Store' not in s]

    for s in sorted(songs):
        meta = get_meta(s)

        song_num = s.split('/')[-1]

        post = glob.glob('source/_posts/%s*' % song_num)
        if post:
            print('%s 已存在' % song_num)
            continue

        if not meta.get('ytid'):
            print('%s 尚未发布' % song_num)
            continue

        nowtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        cmd = 'cp "%s" "%s"' % (s+'/cover.jpg', 'themes/edinburgh/source/post_covers/%s.jpg' % song_num)
        if os.system(cmd) != 0:
            print('指令执行失败:', cmd)
            exit(1)

        new_post_path = 'source/_posts/%s-%s.md' % (song_num, meta['title'].replace(' ', '-').lower())
        with open(new_post_path, 'w') as f:
            f.write(
                post_template % (meta['title'], nowtime, song_num, meta['tags'], meta['ytid'])
            )
            print('%s 生成POST' % song_num)
