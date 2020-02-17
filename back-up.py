# -*- coding:utf8 -*-
# %%
import os
import shutil
import re
# %%
private_back_up_dir = 'D:\\github\\private-blog-back-up'
blog_dir = 'D:\\github\\blog'
blog_back_up_dir = 'D:\\github\\blog\\blog-back-up'

extraSet = {'.deploy_git', '.git', '.history', '.vscode', 'node_modules', 'public', 'landscape', 'blog-back-up', 'desktop.ini'}

# %%
class Traverse:
    """
    This class is used to operate my blog file and take them a back-up
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def copy_file(self, work_dir, target_dir):
        for file in os.listdir(work_dir):
            srcFile = os.path.join(work_dir, file)
            targetFile = os.path.join(target_dir, file)
            if os.path.isfile(srcFile):
                print(os.path.join(work_dir, file))
                if self.extra(extraSet, srcFile):
                    shutil.copy(srcFile, targetFile)
            elif os.path.isdir(srcFile):
                print(os.path.join(work_dir,file))
                if self.extra(extraSet, srcFile):
                    if os.path.exists(targetFile) == False:
                        os.makedirs(targetFile)
                        self.copy_file(srcFile, targetFile)

    def extra(self, extraSet, targetPath):
        pathDir = re.split('\\\\', targetPath)
        for dir in pathDir:
            if dir in extraSet:
                return False
        return True
    
    def remove(self, workdir):
        for file in os.listdir(workdir):
            filePath = os.path.join(workdir, file)
            print("remove: " + filePath)
            if os.path.isfile(filePath) and file != 'desktop.ini':
                os.remove(filePath)
            elif os.path.isdir(filePath) and file != '.git':
                shutil.rmtree(filePath)

    def git_operation(self, target_dir):
        '''
        git 命令行函数，将仓库提交

        ----------
        '''
        print(os.getcwd())
        os.chdir(target_dir)
        print(os.getcwd())
        os.system('git add .')
        os.system('git commit -m "update"')
        os.system('git push origin master')
# %%
class Copy_posts:
    """
    This class is used to copy _posts to blog-back-up
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def copy_posts(self, source_dir, target_dir):
        for files in os.listdir(source_dir):
            srcFile = os.path.join(source_dir, files)
            tarFile = os.path.join(target_dir, files)
            if os.path.isfile(srcFile) and os.path.splitext(srcFile)[1] != '.md':
                print(tarFile)
                shutil.copy(srcFile, tarFile)
            if os.path.isdir(srcFile):
                if os.path.exists(tarFile) == False:
                    os.makedirs(tarFile)
                    self.copy_posts(srcFile, tarFile)

    def remove_posts(self, work_dir):
        for file in os.listdir(work_dir):
            tarFilePath = os.path.join(work_dir, file)
            shutil.rmtree(tarFilePath)

# %%
if __name__ == "__main__":
    traverse = Traverse()
    traverse.remove(private_back_up_dir)
    traverse.copy_file(blog_dir, private_back_up_dir)
    traverse.git_operation(private_back_up_dir)

    copyPosts = Copy_posts()
    postsDir = os.path.join(blog_dir, 'source\\_posts')
    tarPostsDir = os.path.join(blog_back_up_dir, '_posts')
    shutil.rmtree(tarPostsDir)
    copyPosts.copy_posts(postsDir, tarPostsDir)

