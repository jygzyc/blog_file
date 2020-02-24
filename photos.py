# -*- coding:utf8 -*-
# %%
from PIL import Image
from glob import glob
import os
import math
import shutil
import re
# %%
threshold = 1.5 * 1024 * 1024
blog_file_dir = os.path.dirname(os.path.abspath(__file__))
source_photos_dir = os.path.join(blog_file_dir, "originPhotos")
target_photos_dir = os.path.join(blog_file_dir, "photos")
blog_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# %%
class ImageProcess:

    """
    This class is used to read photos and compress them
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def resize_images(self, source_dir, target_dir, threshold):
        
        '''
        以2M为阈值压缩图片，并放入新的文件夹中 \n
        threshold: 阈值
        '''
        filenames = glob('{}/*'.format(source_dir))
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        for filename in filenames:
            filesize = os.path.getsize(filename)
            if filesize >= threshold: 
                with Image.open(filename) as im:
                    width, height = im.size
                    if width >= height:
                        new_width = int(math.sqrt(threshold/2))
                        new_height = int(new_width * height * 1.0 / width)
                    else:
                        new_height = int(math.sqrt(threshold/2))
                        new_width = int(new_height * width * 1.0 / height)
                    resized_im = im.resize((new_width, new_height))
                    output_filename = filename.replace(source_dir, target_dir)
                    resized_im.save(output_filename)
            else:
                with Image.open(filename) as im:
                    output_filename = filename.replace(source_dir, target_dir)
                    im.save(output_filename)
    def remove_photos(self, workdir):
        if os.path.exists(workdir):
            shutil.rmtree(workdir)


class Copy_posts:
    """
    This class is used to copy `_posts` to blog_file_dir
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def copy_posts(self, source_dir, target_dir):
        for files in os.listdir(source_dir):
            srcFile = os.path.join(source_dir, files)
            tarFile = os.path.join(target_dir, files)
            if os.path.isfile(srcFile) and os.path.splitext(srcFile)[1] != '.md':
                shutil.copy(srcFile, tarFile)
            if os.path.isdir(srcFile):
                if os.path.exists(tarFile) == False:
                    os.makedirs(tarFile)
                    self.copy_posts(srcFile, tarFile)
    def remove_posts(self, workdir):
        if os.path.exists(workdir):
            shutil.rmtree(workdir)

def changeDir(target_dir):
    '''
    change work dir
    '''
    os.chdir(target_dir)
    print(os.getcwd())

def git_operation():
    '''
    git 命令行函数，将仓库提交

    ----------
    git add . \n
    git commit -m "update" \n
    git push origin master \n
    '''
    os.system('git add .')
    os.system('git commit -m "update"')
    os.system('git push origin master')

# %%
if __name__ == "__main__":
    print("---- Image Process Start----")
    imm = ImageProcess()
    imm.remove_photos(target_photos_dir)
    imm.resize_images(source_photos_dir, target_photos_dir, threshold)
    print("---- Image Process Over----")
    print("---- _posts Process Start----")
    copyPosts = Copy_posts()
    postsDir = os.path.join(blog_dir, 'source\\_posts')
    tarPostsDir = os.path.join(blog_file_dir, '_posts')
    copyPosts.remove_posts(tarPostsDir)
    copyPosts.copy_posts(postsDir, tarPostsDir)
    print("---- _posts Process Over----")
    changeDir(blog_file_dir)
    git_operation()

# %%
