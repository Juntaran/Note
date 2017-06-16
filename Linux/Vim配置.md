# Vim配置

*2017.6.16*

## 1. 导入

    wget -qO- https://raw.github.com/ma6174/vim/master/setup.sh | sh -x
    
## 2. 覆盖 ~/.vimrc

    wget -O vim.tar.gz https://raw.githubusercontent.com/Juntaran/Note/master/Linux/vim.tar.gz
    tar -zxvf vim.tar.gz
    mv ~/.vimrc ~/.vimrc_bak
    mv vimrc ~/.vimrc
    rm -rf vimrc vim.tar.gz