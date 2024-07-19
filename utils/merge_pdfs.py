import os
import pdfkit
from bs4 import BeautifulSoup
import requests

list = ['Welcome191.html',
        'ReleaseNotes%20-19-2.02.1.html',
        'ReleaseNotes%20-19-2.02.2.html',
        'ReleaseNotes%20-19-2.02.3.html',
        'chapterTitle-SysRequirements.html',
        'SupportedPlatforms.html',
        'WebBrowser.html',
        'XinetPlugins.html',
        'SupportedFileFormats.html',
        'SupportInformation.html',
        'chapterTitle-ClientGuide.html',
        'Client_Introduction.html',
        'BeforeYouBegin1811.11.1.html',
        'BeforeYouBegin1811.11.2.html',
        'BeforeYouBegin1811.11.3.html',
        'BeforeYouBegin1811.11.4.html',
        'BeforeYouBegin1811.11.5.html',
        'UsingPortal.12.01.html',
        'UsingPortal.12.02.html',
        'UsingPortal.12.03.html',
        'UsingPortal.12.04.html',
        'UsingPortal.12.05.html',
        'UsingPortal.12.06.html',
        'UsingPortal.12.07.html',
        'UsingPortal.12.08.html',
        'UsingPortal.12.09.html',
        'UsingPortal.12.10.html',
        'UsingPortal.12.11.html',
        'UsingPortal.12.12.html',
        'UsingPortal.12.13.html',
        'UsingPortal.12.14.html',
        'UsingPortal.12.15.html',
        'UsingPortal.12.16.html',
        'UsingPortal.12.17.html',
        'UsingPortal.12.18.html',
        'UsingPortal.12.19.html',
        'UsingPortal.12.20.html',
        'UsingPortal.12.21.html',
        'UsingPortal.12.22.html',
        'UsingPortal.12.23.html',
        'UsingPortal.12.24.html',
        'UsingPortal.12.25.html',
        'UsingPilot.13.01.html',
        'UsingPilot.13.02.html',
        'UsingPilot.13.03.html',
        'UsingPilot.13.04.html',
        'UsingPilot.13.05.html',
        'UsingPilot.13.06.html',
        'UsingPilot.13.07.html',
        'UsingPilot.13.08.html',
        'UsingPilot.13.09.html',
        'UsingPilot.13.10.html',
        'UsingPilot.13.11.html',
        'UsingPilot.13.12.html',
        'UsingPilot.13.13.html',
        'UsingPilot.13.14.html',
        'UsingPilot.13.15.html',
        'UsingPilot.13.16.html',
        'UsingPilot.13.17.html',
        'UsingPilot.13.18.html',
        'UsingPilot.13.19.html',
        'App_TroubleshootOSX-NEW.14.1.html',
        'App_TroubleshootOSX-NEW.14.2.html',
        'App_TroubleshootOSX-NEW.14.3.html',
        'App_TroubleshootOSX-NEW.14.4.html',
        'App_TroubleshootOSX-NEW.14.5.html',
        'App_TroubleshootInDesignNEW.html',
        'App_TroubleshootPhotoshop.html',
        'App_TroubleshootIllustrator.html',
        'App_ExternalLinks.18.1.html',
        'App_ExternalLinks.18.2.html',
        'App_ExternalLinks.18.3.html',
        'App_ExternalLinks.18.4.html',
        'App_ExternalLinks.18.5.html',
        'App_ExternalLinks.18.6.html',
        'App_ExternalLinks.18.7.html',
        'chapterTitle-AdminGuide.html',
        'WebNative_intro.html',
        'Install_license.21.01.html',
        'Install_license.21.02.html',
        'Install_license.21.03.html',
        'Install_license.21.04.html',
        'Install_license.21.05.html',
        'Install_license.21.06.html',
        'License_Encoding.html',
        'Install_license.21.08.html',
        'Install_license.21.09.html',
        'Install_license.21.10.html',
        'Install_license.21.11.html',
        'Install_license.21.12.html',
        'Install_license.21.13.html',
        'Install_license.21.14.html',
        'Install_license.21.15.html',
        'Install_license.21.16.html',
        'Install_license.21.17.html',
        'File_sys_org.html',
        'Web_server.23.1.html',
        'Web_server.23.2.html',
        'Web_server.23.3.html',
        'Web_server.23.4.html',
        'Web_server.23.5.html',
        'Vol_conventions.html',
        'VolumesUsers_SystemVolumes_Summary.html',
        'VolumesUsers_SystemVolumes_Edit.html',
        'VolumesUsers_SystemVolumes_NewSystemVolume.html',
        'VolumesUsers_SystemVolumes_PreviewSetting.html',
        'Volumes.25.5.html',
        'Volumes.25.6.html',
        'Volumes.25.7.html',
        'VolumesUsers_SystemVolumes_UpdatePreviews.html',
        'Volumes.25.9.html',
        'Users.26.1.html',
        'VolumesUsers_Users_Summary.html',
        'VolumesUsers_Users_NewUser.html',
        'VolumesUsers_Users_EditUser.html',
        'Users.26.5.html',
        'Users.26.6.html',
        'Users.26.7.html',
        'Users.26.8.html',
        'VolumesUsers_Users_SubAdmin.html',
        'User_volumes.27.1.html',
        'VolumesUsers_UserVolumes_NewVolume.html',
        'SMB2_ConnectedUsers.html',
        'SMB.28.2.html',
        'AFPAccess_AppleShareService_ServerOptions.html',
        'VolumesUsers_Groups_Summary.html',
        'VolumesUsers_Groups_NewGroup.html',
        'VolumesUsers_Groups_EditGroup.html',
        'Groups.30.4.html',
        'VolumesUsers_Styles_Styles.html',
        'User_styles.31.2.html',
        'User_styles.31.3.html',
        'User_styles.31.4.html',
        'VolumesUsers_Plugins_Plugins.html',
        'User_plugins.32.2.html',
        'User_plugins.32.3.html',
        'User_plugins.32.4.html',
        'User_plugins.32.5.html',
        'VolumesUsers_Permissions_UsersPermissions.html',
        'VolumesUsers_Permissions_EditUserPermissions.html',
        'User_permissions_PilotUploader.html',
        'Security.35.1.html',
        'Security.35.2.html',
        'Security.35.3.html',
        'Security.35.4.html',
        'Security.35.5.html',
        'SSOMac.36.1.html',
        'SSOMac.36.2.html',
        'SSOMac.36.3.html',
        'SSOMac.36.4.html',
        'SSOMac.36.5.html',
        'SSOMac.36.6.html',
        'SSOLinux.37.1.html',
        'SSOLinux.37.2.html',
        'SSOLinux.37.3.html',
        'SSOLinux.37.4.html',
        'SSOLinux.37.5.html',
        'SSOLinux.37.6.html',
        'VolumesUsers_SystemVolumes_VideoSettings.html',
        '01.vsp.38.2.html',
        '02.vsp.html',
        '03.vsp.html',
        '04.VSP_workflow.html',
        'DB_overview.42.1.html',
        'DB_overview.42.2.html',
        'DB_overview.42.3.html',
        'DB_overview.42.4.html',
        'DB_overview.42.5.html',
        'DB_overview.42.6.html',
        'DB_admin.43.01.html',
        'DB_admin.43.02.html',
        'Database_Admin_Summary.html',
        'Database_Admin_Settings.html',
        'Database_Admin_Stats.html',
        'Database_Admin_FileHistory.html',
        'Database_Admin_QuickSync.html',
        'Database_Admin_Backup.html',
        'Database_Admin_TableCheck.html',
        'DB_admin.43.10.html',
        'DB_admin.43.11.html',
        'Database_Admin_Searching.html',
        'DB_admin_Solr.44.2.html',
        'DB_admin_Solr.44.3.html',
        'DB_admin_Solr.44.4.html',
        'DB_admin_Solr.44.5.html',
        'DB_admin_Solr.44.6.html',
        'Database_DataFields_Summary.html',
        'DB_fields.45.02.html',
        'DB_fields.45.03.html',
        'Database_DataFields_EditFields.html',
        'Database_DataFields_NewField.html',
        'DB_fields.45.06.html',
        'Database_DataFields_DataFieldSets.html',
        'Database_DataFields_NewFieldSet.html',
        'Database_DataFields_EditFieldSet.html',
        'Database_DataFields_FileInfoPanels.html',
        'Database_Templates_Summary.html',
        'DB_templates.46.2.html',
        'DB_templates.46.3.html',
        'Database_Templates_EditTemplate.html',
        'DB_templates.46.5.html',
        'Database_Templates_NewTemplate.html',
        'Database_PermissionSets_Summary.html',
        'DB_perms.47.2.html',
        'DB_perms.47.3.html',
        'Database_PermissionSets_EditPermisionSet.html',
        'Database_PermissionSets_NewPermissionSet.html',
        'Database_PersmissionSets_EditPermissionSet.html',
        'Database_Actions_EditSetting.html',
        'Triggers_Actions_Quick.48.2.html',
        'Database_Actions_Summary.html',
        'Database_Actions_NewSetting.html',
        'Database_TriggerSets_Summary.html',
        'Database_TriggerSets_NewTriggerSet.html',
        'Triggers_Actions_Quick.48.7.html',
        'Database_TriggerSets_EditTriggerSet.html',
        'Triggers_Actions.49.1.html',
        'Triggers_Actions.49.2.html',
        'Triggers_Actions.49.3.html',
        'Triggers_Actions.49.4.html',
        'Triggers_Actions.49.5.html',
        'Triggers_Actions.49.6.html',
        'Triggers_Actions.49.7.html',
        'Triggers_Actions.49.8.html',
        'Triggers_Actions.49.9.html',
        'Archive_disk.html',
        'Triggers_custom.51.01.html',
        'Triggers_custom.51.02.html',
        'Triggers_custom.51.03.html',
        'Triggers_custom.51.04.html',
        'Triggers_custom.51.05.html',
        'Triggers_custom.51.06.html',
        'Triggers_custom.51.07.html',
        'Triggers_custom.51.08.html',
        'Triggers_custom.51.09.html',
        'Triggers_custom.51.10.html',
        'BusinessRules.52.1.html',
        'BusinessRules.52.2.html',
        'Database_Filters_Summary.html',
        'BusinessRules-config.53.1.html',
        'BusinessRules-config.53.2.html',
        'Data_read.54.1.html',
        'Data_read.54.2.html',
        'Data_read.54.3.html',
        'Data_read.54.4.html',
        'Data_import.55.1.html',
        'Data_import.55.2.html',
        'Data_import.55.3.html',
        'Data_export.html',
        'DB_troubleshoot.57.01.html',
        'DB_troubleshoot.57.02.html',
        'DB_troubleshoot.57.03.html',
        'DB_troubleshoot.57.04.html',
        'DB_troubleshoot.57.05.html',
        'DB_troubleshoot.57.06.html',
        'DB_troubleshoot.57.07.html',
        'DB_troubleshoot.57.08.html',
        'DB_troubleshoot.57.09.html',
        'DB_troubleshoot.57.10.html',
        'PrintHotFolder_QueueStatus_Summary.html',
        'Queue_monitor.58.2.html',
        'PrintHotFolder_QueueStatus_PendingJobs.html',
        'PrintHotFolder_QueueStatus_CompletedJobLogs.html',
        'PrintHotFolder_PrintQueues_Summary.html',
        'Print_queues.59.2.html',
        'PrintHotFolder_PrintQueues_EditQueue.html',
        'PrintHotFolder_PrintQueues_NewQueue.html',
        'Print_queues.59.5.html',
        'Print_queues.59.6.html',
        'PrintHotFolder_Spoolers_Summary.html',
        'PrintHotFolder_Spoolers_EditSpooler.html',
        'PrintHotFolder_Spoolers_MakeNewSpooler.html',
        'PrintHotFolder_HotFolders_Summary.html',
        'PrintHotFolder_HotFolders_EditHotFolder.html',
        'PrintHotFolder_HotFolders_MakeNewHotFolder.html',
        'Hot_folders.61.4.html',
        'PrintHotFolder_GeneralAdmin.html',
        'Color_settings.63.1.html',
        'Color_settings.63.2.html',
        'Color_settings.63.3.html',
        'PrintHotFolder_ColorSettings_Edit.html',
        'PDF_IR.64.1.html',
        'PDF_IR.64.2.html',
        'PDF_IR.64.3.html',
        'PDF_IR.64.4.html',
        'PDF_IR.64.5.html',
        'PDF_IR.64.6.html',
        'ACLs.65.1.html',
        'ACLs.65.2.html',
        'ACLs.65.3.html',
        'AFPAccess_AccessRestriction_Summary.html',
        'AFPAccess_AccessRestriction_Edit.html',
        'AFPAccess_AccessRestriction_NewACL.html',
        'License.66.1.html',
        'License_License_XinetLicense.html',
        'License_License_SendLicenseRequest.html',
        'License_License_InstallNewLicense.html',
        'Logging_Status.html',
        'Xinet_system.67.02.html',
        'Logging_XinetSystem.html',
        'Logging_PreviewGeneration.html',
        'Logging_PreviewGeneration_Syncing_History.html',
        'Logging_WebAccess.html',
        'Logging_Database.html',
        'Logging_Triggers.html',
        'Logging_PrintDaemon.html',
        'Logging_TableCheck.html',
        'Logging_Settings_WebAccess.html',
        'Maintenance.html',
        'Appen_command_line.69.01.html',
        'Appen_command_line.69.02.html',
        'Appen_command_line.69.03.html',
        'Appen_command_line.69.04.html',
        'Appen_command_line.69.05.html',
        'Appen_command_line.69.06.html',
        'Appen_command_line.69.07.html',
        'Appen_command_line.69.08.html',
        'Appen_command_line.69.09.html',
        'Appen_command_line.69.10.html',
        'Appen_command_line.69.11.html',
        'Appen_command_line.69.12.html',
        'Appen_command_line.69.13.html',
        'Appen_command_line.69.14.html',
        'Appen_command_line.69.15.html',
        'Appen_command_line.69.16.html',
        'Appen_command_line.69.17.html',
        'Appen_command_line.69.18.html',
        'Appen_command_line.69.19.html',
        'Appen_command_line.69.20.html',
        'Appen_command_line.69.21.html',
        'Appen_command_line.69.22.html',
        'Appen_command_line.69.23.html',
        'Appen_command_line.69.24.html',
        'Appen_command_line.69.25.html',
        'Appen_command_line.69.26.html',
        'Appen_command_line.69.27.html',
        'Appen_command_line.69.28.html',
        'Appen_command_line.69.29.html',
        'Appen_command_line.69.30.html',
        'Appen_command_line.69.31.html',
        'Appen_command_line.69.32.html',
        'Appen_command_line.69.33.html',
        'Appen_command_line.69.34.html',
        'Appen_command_line.69.35.html',
        'Appen_command_line.69.36.html',
        'Appen_command_line.69.37.html',
        'Appen_command_line.69.38.html',
        'Appen_command_line.69.39.html',
        'Appen_command_line.69.40.html',
        'Appen_command_line.69.41.html',
        'Appen_command_line.69.42.html',
        'Appen_command_line.69.43.html',
        'Appen_command_line.69.44.html',
        'Appen_command_line.69.45.html',
        'Appen_command_line.69.46.html',
        'Appen_command_line.69.47.html',
        'Appen_command_line.69.48.html',
        'Appen_command_line.69.49.html',
        'Appen_command_line.69.50.html',
        'Appen_command_line.69.51.html',
        'Appen_command_line.69.52.html',
        'Appen_command_line.69.53.html',
        'Appen_command_line.69.54.html',
        'Appen_command_line.69.55.html',
        'Appen_command_line.69.56.html',
        'Appen_command_line.69.57.html',
        'Appen_FP_command_line.70.1.html',
        'Appen_FP_command_line.70.2.html',
        'Appen_FP_command_line.70.3.html',
        'Appen_drag_drop.71.1.html',
        'Appen_drag_drop.71.2.html',
        'Appen_drag_drop.71.3.html',
        'Appen_drag_drop.71.4.html',
        'Appen_db_syncs.72.1.html',
        'Appen_db_syncs.72.2.html',
        'Appen_db_syncs.72.3.html',
        'Appen_db_syncs.72.4.html',
        'Appen_db_syncs.72.5.html',
        'Appen_Conversions.html',
        'chapterTitle-PortalAdmin.html',
        'Portal_Edit.html',
        'Portal_Summary.html',
        'Portal.75.3.html',
        'Portal.75.4.html',
        'Portal.75.5.html',
        'Portal.75.6.html',
        'Adding or Removing Portal Server Sites","Portal_Add.html',
        'Portal.75.8.html',
        '02B.WN_Portal_sites.76.1.html',
        '02B.WN_Portal_sites.76.2.html',
        '02B.WN_Portal_sites.76.3.html',
        '02B.WN_Portal_sites.76.4.html',
        '02B.WN_Portal_sites.76.5.html',
        '02B.WN_Portal_sites.76.6.html',
        '02A.Marquee.77.1.html',
        '02A.Marquee.77.2.html',
        '02A2.Theme_Editor.78.1.html',
        '02A2.Theme_Editor.78.2.html',
        'Appen_B_TE_Exhb.html',
        '03.WN_Portal_custom.80.1.html',
        '03.WN_Portal_custom.80.2.html',
        '03.WN_Portal_custom.80.3.html',
        '03.WN_Portal_custom.80.4.html',
        '03.WN_Portal_custom.80.5.html',
        '03.WN_Portal_custom.80.6.html',
        '04.WN_Portal_Adv.81.1.html',
        '04.WN_Portal_Adv.81.2.html',
        '04.WN_Portal_Adv.81.3.html',
        '05.WN_Features.82.1.html',
        '05.WN_Features.82.2.html',
        'Appen_A_Tags.83.1.html',
        'Appen_A_Tags.83.2.html',
        'Appen_A_Tags.83.3.html',
        'Appen_A_Tags.83.4.html',
        'chapterTitle-Copyright.84.1.html',
        'chapterTitle-Copyright.84.2.html',
        'chapterTitle-Copyright.84.3.html']

base_url = "https://docs.xinet.com/docs/Xinet/19.2.1/AllGuides/wwhelp/wwhimpl/js/html/wwhelp.htm#href="

for one_html in list:
    url = base_url+one_html
    page_response = requests.get(url)
    html_file = f"xinet_docs/{one_html.split('/')[-1]}"

    with open(html_file, 'w', encoding='utf-8') as file:
        file.write(page_response.text)


# Directory to save HTML and PDF files
os.makedirs('xinet_docs', exist_ok=True)



