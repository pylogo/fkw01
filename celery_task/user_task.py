# 使用celery
from celery import Celery
from django.conf import settings
from django.core.mail import send_mail
from fkw_v1 import settings

# 创建一个Celery类的实列化对象
# 第一个参数可以随便写，通常写路径
# 第二个参数指定存放

# 一定要配置启动文件
import os
import django

# 这一段在wsgi中
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fkw_v1.settings")
django.setup()
from celery_task.celery import APP


# 定义任务函数
@APP.task
def send_register_active_email(to_email, username, token):
    # 发邮件
    subject = '验证木柯发卡网账户'
    html_message = r'''
                       <html>
               <head>
                   <base target="_blank">
                   <style type="text/css">
                       ::-webkit-scrollbar {
                           display: none;
                       }
                   </style>
                   <style id="cloudAttachStyle" type="text/css">
                       #divNeteaseBigAttach, #divNeteaseBigAttach_bak {
                           display: none;
                       }
                   </style>

               </head>
               <body tabindex="0" role="listitem">


               <style type="text/css">
                   #outlook a {
                       padding: 0;
                       color: inherit;
                   }

                   .ReadMsgBody {
                       width: 100%;
                   }

                   .ExternalClass {
                       width: 100%;
                   }

                   .ExternalClass,
                   .ExternalClass span,
                   .ExternalClass td,
                   .ExternalClass div {
                       line-height: 100%;
                   }

                   body,
                   table,
                   td,
                   a {
                       -webkit-text-size-adjust: 100%;
                       -ms-text-size-adjust: 100%;
                   }

                   table,
                   td {
                       mso-table-lspace: 0pt;
                       mso-table-rspace: 0pt;
                   }

                   img {
                       -ms-interpolation-mode: bicubic;
                   }

                   body {
                       background-color: #f2f2f2;
                       font-family: Helvetica, Arial, sans-serif;
                       height: 100% !important;
                       margin: 0 !important;
                       padding: 0 !important;
                       width: 100% !important;
                   }

                   img {
                       border: 0;
                       height: auto;
                       line-height: 100%;
                       outline: none;
                       text-decoration: none;
                   }

                   a[x-apple-data-detectors] {
                       color: inherit !important;
                       text-decoration: none !important;
                       font-size: inherit !important;
                       font-family: inherit !important;
                       font-weight: inherit !important;
                       line-height: inherit !important;
                   }

                   .webkit-hide {
                       display: none !important;
                   }

                   .webkit-show {
                       height: auto !important;
                       width: auto !important;
                       max-width: none !important;
                       max-height: none !important;
                       overflow: auto !important;
                       visibility: visible !important;
                       display: block !important;
                   }

                   #font-weight-normal {
                       font-weight: normal !important;
                   }

                   .link-hover:hover {
                       text-decoration: none !important;
                   }

                   h1 {
                       font-size: 22px !important;
                       font-weight: 700 !important;
                       padding: 0 0 0 0 !important;
                   }

                   .green-btn {
                       color: #fff;
                       display: inline-block;
                       font-size: 14px;
                       font-weight: 500;
                       line-height: 1.07;
                       text-align: center;
                       background: #7ac70c;
                       border-radius: 40px;
                       padding: 11px 25px;
                       min-width: 150px;
                       text-decoration: none;
                       text-transform: uppercase;
                   }

                   _media screen and

                   (
                   max-width:

                   609
                   px

                   )
                   {
                   body[yahoo] .deviceWidth {
                       width: 100% !important;
                       padding: 0;
                       min-width: 100% !important;
                   }

                   .mobile-hide {
                       display: none !important;
                   }

                   .mobile-center {
                       text-align: center !important;
                   }

                   .mobile-center2 {
                       margin: 0 auto;
                   }


                   td.mobile-show {
                       display: table-cell !important;
                   }

                   .img-max {
                       max-width: 100% !important;
                       height: auto !important;
                   }

                   .img-max2 {
                       width: 100% !important;
                       max-width: 100% !important;
                       height: auto !important;
                   }

                   .responsive-table {
                       width: 100% !important;
                       max-width: 100% !important;
                   }

                   .email-container {
                       padding: 10px !important;
                   }

                   }
               </style>


               <table border="0" cellpadding="0" cellspacing="0" width="100%" class="email-container">

                   <tbody>
                   <tr>
                       <td bgcolor="#f2f2f2" align="center" class="section-padding" style="padding:0 5px !important;">


                           <table border="0" cellpadding="0" cellspacing="0" width="600" class="deviceWidth"
                                  style=" width:100%; max-width:600px; min-height:30px;">
                               <tbody>
                               <tr>
                                   <td height="30" style="height:30px; min-height:30px; line-height:30px; font-size:20px;">&nbsp;</td>
                               </tr>
                               <tr>
                                   <td align="center">
                                       <img class="brand-logo-img"
                                            src="https://www.cnblogs.com/images/cnblogs_com/limengda/1456199/o_WechatIMG3.png" width="199"
                                            height="auto"
                                            start="display:block; border:0px;text-decoration: none;  border-style: none;  color: #ffffff; padding-right: 10px; border-width:0;">
                                   </td>
                               </tr>
                               <tr>
                                   <td height="20" style="height:20px; min-height:20px; line-height:20px; font-size:20px;">&nbsp;</td>
                               </tr>
                               </tbody>
                           </table>


                           <table border="0" cellpadding="0" cellspacing="0" width="100%" class="max-width"
                                  style="max-width: 600px; border-radius:20px;  box-shadow: 0 2px 10px 5px rgba(0, 0, 0, 0.05);">
                               <tbody>
                               <tr>
                                   <td align="center" style="-webkit-border-radius:20px;-moz-border-radius:20px;border-radius:20px; ">
                                       <table cellpadding="0" cellspacing="0" border="0" width="100%"
                                              style="-webkit-border-radius:20px;-moz-border-radius:20px;border-radius:20px; ">
                                           <tbody>
                                           <tr>
                                               <td colspan="3" class="banner-wrapper" style="text-align: center;">
                                                   <img class="banner"
                                                        src="http://static.duolingo.com/images/email/verification/header.png"
                                                        width="100%" style="display: block; margin: 0; border: 0; max-width: 600px;">
                                               </td>
                                           </tr>
                                           <tr>
                                               <td bgcolor="#FFFFFF" width="7%"
                                                   style="width:7%; min-width:30px; -webkit-border-radius:0 0 0 20px;-moz-border-radius:0 0 0 20px;border-radius:0 0 0 20px; ">
                                                   &nbsp;
                                               </td>
                                               <td class="inner" bgcolor="#ffffff" style="background-color: #ffffff; padding: 5%;">
                                                   <table id="intro" border="0" cellspacing="0" cellpadding="0"
                                                          style="width: 100%; margin: 0 auto;">
                                                       <tbody>
                                                       <tr>
                                                           <td width="100%" style="max-width:600px">
                                                               <h1 style="font-size: 22px !important; font-weight: 700 !important; padding: 0 0 0 0 !important;">
                                                                   username 验证您的邮箱</h1>
                                                               <p style="color:#999999">
                                                                   username您好，经过验证的帐户可以访问木柯发卡网<br>单击下方按钮以加入！
                                                               </p>
                                                               <br>
                                                           </td>
                                                       </tr>
                                                       <tr>
                                                           <td style="word-break: break-all;" width="100%">

                                                               <a class="green-btn"
                                                                  style="color: #fff;display: inline-block;font-size: 14px;font-weight: 500;line-height: 1.07;text-align: center;background: #7ac70c;border-radius: 40px;padding: 11px 25px;min-width: 150px;text-decoration: none; text-transform: uppercase;"
                                                                  href="http://www.donghaibook.com/user/active/token">确认电子邮件 </a>
                                                               <br>
                                                           </td>
                                                       </tr>
                                                       </tbody>
                                                   </table>
                                               </td>
                                               <td bgcolor="#FFFFFF" width="7%"
                                                   style="width:7%;min-width:30px; -webkit-border-radius:0 0 20px 0; -moz-border-radius:0 0 20px 0; border-radius:0 0 20px 0; ">
                                                   &nbsp;
                                               </td>
                                           </tr>
                                           </tbody>
                                       </table>
                                   </td>
                               </tr>
                               </tbody>
                           </table>


                           <table border="0" cellpadding="0" cellspacing="0" width="100%" class="max-width"
                                  style="max-width: 600px; border-radius:20px;">
                               <tbody>
                               <tr>
                                   <td align="left">
                                       <table cellpadding="0" cellspacing="0" border="0" width="100%">
                                           <tbody>
                                           <tr>
                                               <td colspan="5" height="25"
                                                   style="height:25px; min-height:25px; line-height:25px; font-size:1px;">&nbsp;
                                               </td>
                                           </tr>
                                           <tr>
                                               <td width="3%" style="width:3%; min-width:15px;">&nbsp;</td>

                                               <td width="15" style="width:15px; font-size:15px;">&nbsp;</td>
                                               <td width="3%" style="width:3%;min-width:15px;">&nbsp;</td>
                                           </tr>
                                           <tr>
                                               <td colspan="5" height="30"
                                                   style="height:30px; min-height:30px; line-height:30px; font-size:1px;">&nbsp;
                                               </td>
                                           </tr>
                                           </tbody>
                                       </table>
                                   </td>
                               </tr>
                               </tbody>
                           </table>


                       </td>
                   </tr>
                   </tbody>
               </table>


               <div style="display:none; white-space:nowrap; font:15px courier; color:#ffffff;">

                   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

               </div>


               <style type="text/css">
                   body {
                       font-size: 14px;
                       font-family: arial, verdana, sans-serif;
                       line-height: 1.666;
                       padding: 0;
                       margin: 0;
                       overflow: auto;
                       white-space: normal;
                       word-wrap: break-word;
                       min-height: 100px
                   }

                   td, input, button, select, body {
                       font-family: Helvetica, 'Microsoft Yahei', verdana
                   }

                   pre {
                       white-space: pre-wrap;
                       white-space: -moz-pre-wrap;
                       white-space: -pre-wrap;
                       white-space: -o-pre-wrap;
                       word-wrap: break-word;
                       width: 95%
                   }

                   th, td {
                       font-family: arial, verdana, sans-serif;
                       line-height: 1.666
                   }

                   img {
                       border: 0
                   }

                   header, footer, section, aside, article, nav, hgroup, figure, figcaption {
                       display: block
                   }

                   blockquote {
                       margin-right: 0px
                   }
               </style>


               <style id="ntes_link_color" type="text/css">a, td a {
                   color: #064977
               }</style>

               </body>
               </html>
                       '''.replace('username', username)
    html_message = html_message.replace('token', token)

    message = ''
    recipient_list = [to_email]

    send_mail(subject, message, settings.EMAIL_FROM, recipient_list, html_message=html_message)


# 定义卡密函数
@APP.task
def send_km_active_email(to_email, message1):
    # 发邮件
    subject = '木柯发卡网'
    message = ''
    recipient_list = [to_email]
    html_message = '<h6>%s</h6>' % message1
    send_mail(subject, message, settings.EMAIL_FROM, recipient_list=recipient_list, html_message=html_message)
