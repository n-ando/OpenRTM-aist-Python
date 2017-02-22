#!/bin/sh
#
# @file pkg_install_fedora.sh
# @brief OpenRTM-aist dependent packages install script for Fedora
# @author Noriaki Ando <n-ando@aist.go.jp>
#         Shinji Kurihara
#         Tetsuo Ando
#         Nobu Kawauchi
#         Saburo Takahashi
#
# このシェルスクリプトは、aceおよびomniORBのパッケージをインストールし、
# fedoraの開発環境を構築します。
#
# $Id$
#

# Usage: sudo pkg_install_python_fedora.sh [-u -y -h]
# option -u            : Uninstall tool_packages.
# option -y            : When yes/no prompt for installing would be presente    d, assume that the user entered "yes".
# option -h            : Display a brief help message.
#


#---------------------------------------
# パッケージリスト
#---------------------------------------
version_num=`cat /etc/fedora-release | awk '/Fedora/{print $3}' -`
if [ $version_num -le 19 ]; then
    omnipy="omniORB-servers omniORBpy omniORBpy-devel omniORBpy-standard"
else
    omnipy="omniORB-servers python-omniORB omniORBpy-devel"
fi
devel="python"
openrtm="OpenRTM-aist-Python OpenRTM-aist-Python-example"
packages="$devel $omnipy $openrtm"
u_packages="$omnipy $openrtm "

#---------------------------------------
# yum / dnf コマンド切替え
#---------------------------------------
if [ $version_num -ge 22 ]; then
    COMMAND="dnf"
else
    COMMAND="yum"
fi

#----------------------------------------
# root かどうかをチェック
#----------------------------------------
check_root () {
    if test ! `id -u` = 0 ; then
	echo ""
	echo "This script should be run by root user."
	echo "Abort."
	echo ""
	exit 1
    fi
}

#---------------------------------------
# インストール済パッケージリスト
#---------------------------------------
rpm_qa="/tmp/yum_list.txt"
get_pkg_list () {
    rpm -qa > $rpm_qa
}
clean_pkg_list () {
    rm -f $rpm_qa
}

#---------------------------------------
# リポジトリサイト設定ファイルを生成
#---------------------------------------
openrtm_repo () {
cat <<EOF
[openrtm]
name=Fedora \$releasever - \$basearch
failovermethod=priority
baseurl=http://openrtm.org/pub/Linux/Fedora/releases/\$releasever/Fedora/\$basearch/os/Packages
enabled=1
gpgcheck=0
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-fedora file:///etc/pki/rpm-gpg/RPM-GPG-KEY
EOF
} 
create_repo() {
    repo="/etc/yum.repos.d/openrtm.repo"
    if test ! -f $repo ; then
	echo "OpenRTM-aist のリポジトリが登録されていません。"
	echo "OpenRTM-aist のリポジトリ: "
	echo "  http://www.openrtm.org/pub/Linux/Fedora/"
	read -p "を追加します。よろしいですか？ (y/n) [y] " kick_shell

	if test "x$kick_shell" = "xn" ; then
	    echo "中断します。"
	    exit 0
	else
	    openrtm_repo > /etc/yum.repos.d/openrtm.repo
	fi
    fi
}

#----------------------------------------
# パッケージインストール関数
#----------------------------------------
install_packages () {
    for p in $*; do
	if test "x$p" = "x0.4.2" || test "x$p" = "x0.4.2" ; then
	    :
	else
	    if echo "$p" | grep -q '=0.4.2' ; then
		str=`echo "$p" |sed 's/=0.4.2//'`
	    else
		str="$p"
	    fi

	    ins=`rpm -qa $str`

	    if test "x$ins" = "x"; then
		echo "Now installing: " $p
		$COMMAND install $p $force_yes
		echo "done."
		echo ""
	    else
		if echo "$ins" |grep -q '0.4.2-0' ; then
			$COMMAND install $p
			echo "done."
			echo ""
	       else
 		    echo $ins
		    echo $str "is already installed."
		    echo ""
		fi
	    fi
	fi
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
	echo "Now uninstalling: " $p
	$COMMAND erase $p
	echo "done."
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

check_root

if test "x$1" = "x-y" ; then
    force_yes="-y"
fi

if test "x$1" = "x-u" ; then
    uninstall_packages `reverse $u_packages`
else
    create_repo
    install_packages $packages
fi
