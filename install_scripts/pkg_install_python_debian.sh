#!/bin/sh
#
# @file pkg_install_debian.sh
# @brief OpenRTM-aist dependent packages install script for Debian-sarge
# @author Noriaki Ando <n-ando@aist.go.jp>
#         Shinji Kurihara
#         Tetsuo Ando
#         Harumi Miyamoto
#         Nobu Kawauchi
#         Saburo Takahashi
#

# Usage: sudo pkg_install_python_debian.sh [-u -y -h]
# option -u            : Uninstall tool_packages.
# option -y            : When yes/no prompt for installing would be presente    d, assume that the user entered "yes".
# option -h            : Display a brief help message.
#


#---------------------------------------
# パッケージリスト
#---------------------------------------
set_package_list()
{
	omnipy="python-omniorb-omg python-omniorb omniidl-python"
	devel="python"
	openrtm="openrtm-aist-python openrtm-aist-python-example"
	packages="$devel $omnipy $openrtm"
	u_packages="$omnipy $openrtm "
}

#---------------------------------------
# ロケールの言語確認
#---------------------------------------
check_lang()
{
lang="en"

locale | grep ja_JP > /dev/null && lang="jp"

if test "$lang" = "jp" ;then
    msg1="ディストリビューションを確認してください。\nDebian以外のOSの可能性があります。"
    msg2="コードネーム ： "
    msg3="このOSはサポートされておりません。"
    msg4=" OpenRTM-aistのリポジトリが登録されていません。"
    msg5="Source.listにOpenrRTM-aistのリポジトリ："
    msg6="を追加します。よろしいですか？ (y/n) [y] "
    msg7="中断します。"
    msg8="ルートユーザーで実行してください。"
    msg9="インストール中です..."
    msg10="完了"
    msg11="アンインストール中です"
else
    msg1="This distribution may not be debian/ubuntu."
    msg2="The code name is : "
    msg3="This OS is not supported."
    msg4="No repository entry for OpenRTM-aist is configured in your system."
    msg5="repository entry for OpenrRTM-aist: "
    msg6="Do you want to add the repository entry for OpenrRTM-aist in source.list? (y/n) [y] "
    msg7="Abort."
    msg8="This script should be run as root."
    msg9="Now installing: "
    msg10="done."
    msg11="Now uninstalling: "

fi

}

#---------------------------------------
# コードネーム取得
#---------------------------------------
check_codename () {
    cnames="sarge etch lenny squeeze wheezy jessie"
    for c in $cnames; do
	if test -f "/etc/apt/sources.list"; then
	    res=`grep $c /etc/apt/sources.list`
	else
	    echo $msg1
	    exit
	fi
	if test ! "x$res" = "x" ; then
	    code_name=$c
	fi
    done
    if test ! "x$code_name" = "x"; then
	echo $msg2 $code_name
    else
	echo $msg3
	exit
    fi
}

#---------------------------------------
# リポジトリサーバ
#---------------------------------------
create_srclist () {
    openrtm_repo="deb http://openrtm.org/pub/Linux/debian/ $code_name main"
}

#---------------------------------------
# ソースリスト更新関数の定義
#---------------------------------------
update_source_list () {
    rtmsite=`grep openrtm /etc/apt/sources.list`
    if test "x$rtmsite" = "x" ; then
	echo $msg4
	echo $msg5
	echo "  " $openrtm_repo
	read -p $msg6 kick_shell

	if test "x$kick_shell" = "xn" ; then
	    echo $msg7
	    exit 0
	else
	    echo $openrtm_repo >> /etc/apt/sources.list
	fi
    fi
}

#----------------------------------------
# root かどうかをチェック
#----------------------------------------
check_root () {
    if test ! `id -u` = 0 ; then
	echo ""
	echo $msg8
	echo $msg7
	echo ""
	exit 1
    fi
}

#----------------------------------------
# パッケージインストール関数
#----------------------------------------
install_packages () {
    for p in $*; do
	echo $msg9 $p
	apt-get install $p $force_yes
	echo $msg10
	echo ""
    done
}

#------------------------------------------------------------
# リストを逆順にする
#------------------------------------------------------------
reverse () {
    for i in $*; do
	echo $i
    done | sed '1!G;h;$!d'
}

#----------------------------------------
# パッケージをアンインストールする
#----------------------------------------
uninstall_packages () {
    for p in $*; do
	echo $msg11 $p
	aptitude remove $p
	echo $msg10
	echo ""
    done
}

#---------------------------------------
# USAGE
#---------------------------------------
howto_usage(){
    cat << EOF
Usage: sudo $0 [-u -y -h]
       option -u            : Uninstall tool_packages.
       option -y            : When yes/no prompt for installing would be presented, assume that the user entered "yes".
       option -h            : Display a brief help message.
EOF
}

#---------------------------------------
# メイン
#---------------------------------------
if test "x$1" = "x-h" ; then
    howto_usage
    exit 1
fi

check_lang
check_root
check_codename
set_package_list

if test "x$1" = "x-y" ; then
    force_yes="-y --force-yes"
fi

if test "x$1" = "x-u" ; then
    uninstall_packages `reverse $u_packages`
else
    create_srclist
    update_source_list
    apt-get update
    install_packages $packages
fi

