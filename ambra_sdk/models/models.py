"""Ambra SDK models."""

from ambra_sdk.models.generated import Accelerator as AcceleratorG
from ambra_sdk.models.generated import Account as AccountG
from ambra_sdk.models.generated import AccountCanShare as AccountCanShareG
from ambra_sdk.models.generated import AccountMd5Counter as AccountMd5CounterG
from ambra_sdk.models.generated import AccountSamlRole as AccountSamlRoleG
from ambra_sdk.models.generated import Activity as ActivityG
from ambra_sdk.models.generated import Analytics as AnalyticsG
from ambra_sdk.models.generated import Annotation as AnnotationG
from ambra_sdk.models.generated import Appointment as AppointmentG
from ambra_sdk.models.generated import ArchiveStudy as ArchiveStudyG
from ambra_sdk.models.generated import ArchiveStudyAws as ArchiveStudyAwsG
from ambra_sdk.models.generated import ArchiveVault as ArchiveVaultG
from ambra_sdk.models.generated import Audit as AuditG
from ambra_sdk.models.generated import BillingSummary as BillingSummaryG
from ambra_sdk.models.generated import BoxFile as BoxFileG
from ambra_sdk.models.generated import Brand as BrandG
from ambra_sdk.models.generated import BrandNamespace as BrandNamespaceG
from ambra_sdk.models.generated import BrandVanity as BrandVanityG
from ambra_sdk.models.generated import Case as CaseG
from ambra_sdk.models.generated import CaseStatusLock as CaseStatusLockG
from ambra_sdk.models.generated import CaseStudy as CaseStudyG
from ambra_sdk.models.generated import Cluster as ClusterG
from ambra_sdk.models.generated import ClusterAccount as ClusterAccountG
from ambra_sdk.models.generated import ClusterNamespace as ClusterNamespaceG
from ambra_sdk.models.generated import Customcode as CustomcodeG
from ambra_sdk.models.generated import CustomcodeDeploy as CustomcodeDeployG
from ambra_sdk.models.generated import Customfield as CustomfieldG
from ambra_sdk.models.generated import DatabaseScripts as DatabaseScriptsG
from ambra_sdk.models.generated import Destination as DestinationG
from ambra_sdk.models.generated import DestinationBurn as DestinationBurnG
from ambra_sdk.models.generated import DestinationSearch as DestinationSearchG
from ambra_sdk.models.generated import Dicomdata as DicomdataG
from ambra_sdk.models.generated import Dictionary as DictionaryG
from ambra_sdk.models.generated import DictionaryAttach as DictionaryAttachG
from ambra_sdk.models.generated import DictionaryEntry as DictionaryEntryG
from ambra_sdk.models.generated import Drchrono as DrchronoG
from ambra_sdk.models.generated import Engine as EngineG
from ambra_sdk.models.generated import Filter as FilterG
from ambra_sdk.models.generated import FilterShare as FilterShareG
from ambra_sdk.models.generated import Group as GroupG
from ambra_sdk.models.generated import Help as HelpG
from ambra_sdk.models.generated import Hl7 as Hl7G
from ambra_sdk.models.generated import Hl7Accession as Hl7AccessionG
from ambra_sdk.models.generated import Hl7Template as Hl7TemplateG
from ambra_sdk.models.generated import Hl7Transform as Hl7TransformG
from ambra_sdk.models.generated import Keyimage as KeyimageG
from ambra_sdk.models.generated import Link as LinkG
from ambra_sdk.models.generated import LinkCharge as LinkChargeG
from ambra_sdk.models.generated import LinkUsage as LinkUsageG
from ambra_sdk.models.generated import Location as LocationG
from ambra_sdk.models.generated import MailTemplate as MailTemplateG
from ambra_sdk.models.generated import Meeting as MeetingG
from ambra_sdk.models.generated import MeetingUser as MeetingUserG
from ambra_sdk.models.generated import Message as MessageG
from ambra_sdk.models.generated import Namespace as NamespaceG
from ambra_sdk.models.generated import NamespaceChildren as NamespaceChildrenG
from ambra_sdk.models.generated import Node as NodeG
from ambra_sdk.models.generated import NodeConnect as NodeConnectG
from ambra_sdk.models.generated import NodeEvent as NodeEventG
from ambra_sdk.models.generated import NodeProgress as NodeProgressG
from ambra_sdk.models.generated import NpiInviteShare as NpiInviteShareG
from ambra_sdk.models.generated import Order as OrderG
from ambra_sdk.models.generated import OrderSps as OrderSpsG
from ambra_sdk.models.generated import Patient as PatientG
from ambra_sdk.models.generated import Purge as PurgeG
from ambra_sdk.models.generated import Radreport as RadreportG
from ambra_sdk.models.generated import \
    RadreportAnalytics as RadreportAnalyticsG
from ambra_sdk.models.generated import Radreportmacro as RadreportmacroG
from ambra_sdk.models.generated import RadreportTemplate as RadreportTemplateG
from ambra_sdk.models.generated import Role as RoleG
from ambra_sdk.models.generated import Route as RouteG
from ambra_sdk.models.generated import RouteRoundRobin as RouteRoundRobinG
from ambra_sdk.models.generated import RsnaclrDoc as RsnaclrDocG
from ambra_sdk.models.generated import RsnaclrSubset as RsnaclrSubsetG
from ambra_sdk.models.generated import Rsync as RsyncG
from ambra_sdk.models.generated import Setting as SettingG
from ambra_sdk.models.generated import StorageStudy as StorageStudyG
from ambra_sdk.models.generated import Study as StudyG
from ambra_sdk.models.generated import StudyAnalytics as StudyAnalyticsG
from ambra_sdk.models.generated import StudyAttachment as StudyAttachmentG
from ambra_sdk.models.generated import StudyCharge as StudyChargeG
from ambra_sdk.models.generated import StudyComment as StudyCommentG
from ambra_sdk.models.generated import StudyDeleted as StudyDeletedG
from ambra_sdk.models.generated import StudyFetch as StudyFetchG
from ambra_sdk.models.generated import StudyHl7 as StudyHl7G
from ambra_sdk.models.generated import StudyNotReady as StudyNotReadyG
from ambra_sdk.models.generated import StudyPhi as StudyPhiG
from ambra_sdk.models.generated import StudyPush as StudyPushG
from ambra_sdk.models.generated import StudyPushStatus as StudyPushStatusG
from ambra_sdk.models.generated import StudyQuestion as StudyQuestionG
from ambra_sdk.models.generated import StudyShare as StudyShareG
from ambra_sdk.models.generated import StudyShareAi as StudyShareAiG
from ambra_sdk.models.generated import StudyShareRsna as StudyShareRsnaG
from ambra_sdk.models.generated import StudyStar as StudyStarG
from ambra_sdk.models.generated import StudyStatusLock as StudyStatusLockG
from ambra_sdk.models.generated import StudyTiming as StudyTimingG
from ambra_sdk.models.generated import System as SystemG
from ambra_sdk.models.generated import Tag as TagG
from ambra_sdk.models.generated import TagObject as TagObjectG
from ambra_sdk.models.generated import TemplateAssign as TemplateAssignG
from ambra_sdk.models.generated import Terminology as TerminologyG
from ambra_sdk.models.generated import TrainingAccount as TrainingAccountG
from ambra_sdk.models.generated import TrainingUser as TrainingUserG
from ambra_sdk.models.generated import User as UserG
from ambra_sdk.models.generated import UserAccount as UserAccountG
from ambra_sdk.models.generated import UserAws as UserAwsG
from ambra_sdk.models.generated import UserGroup as UserGroupG
from ambra_sdk.models.generated import UserInvite as UserInviteG
from ambra_sdk.models.generated import UserInviteShare as UserInviteShareG
from ambra_sdk.models.generated import UserLocation as UserLocationG
from ambra_sdk.models.generated import Validate as ValidateG
from ambra_sdk.models.generated import Webhook as WebhookG
from ambra_sdk.models.generated import WebhookNode as WebhookNodeG
from ambra_sdk.models.generated import WebhookOnce as WebhookOnceG


class Accelerator(AcceleratorG):
    """Accelerator."""


class Account(AccountG):
    """Account."""


class AccountCanShare(AccountCanShareG):
    """AccountCanShare."""


class AccountMd5Counter(AccountMd5CounterG):
    """AccountMd5Counter."""


class AccountSamlRole(AccountSamlRoleG):
    """AccountSamlRole."""


class Activity(ActivityG):
    """Activity."""


class Analytics(AnalyticsG):
    """Analytics."""


class Annotation(AnnotationG):
    """Annotation."""


class Appointment(AppointmentG):
    """Appointment."""


class ArchiveStudy(ArchiveStudyG):
    """ArchiveStudy."""


class ArchiveStudyAws(ArchiveStudyAwsG):
    """ArchiveStudyAws."""


class ArchiveVault(ArchiveVaultG):
    """ArchiveVault."""


class Audit(AuditG):
    """Audit."""


class BillingSummary(BillingSummaryG):
    """BillingSummary."""


class BoxFile(BoxFileG):
    """BoxFile."""


class Brand(BrandG):
    """Brand."""


class BrandNamespace(BrandNamespaceG):
    """BrandNamespace."""


class BrandVanity(BrandVanityG):
    """BrandVanity."""


class Case(CaseG):
    """Case."""


class CaseStatusLock(CaseStatusLockG):
    """CaseStatusLock."""


class CaseStudy(CaseStudyG):
    """CaseStudy."""


class Cluster(ClusterG):
    """Cluster."""


class ClusterAccount(ClusterAccountG):
    """ClusterAccount."""


class ClusterNamespace(ClusterNamespaceG):
    """ClusterNamespace."""


class Customcode(CustomcodeG):
    """Customcode."""


class CustomcodeDeploy(CustomcodeDeployG):
    """CustomcodeDeploy."""


class Customfield(CustomfieldG):
    """Customfield."""


class DatabaseScripts(DatabaseScriptsG):
    """DatabaseScripts."""


class Destination(DestinationG):
    """Destination."""


class DestinationBurn(DestinationBurnG):
    """DestinationBurn."""


class DestinationSearch(DestinationSearchG):
    """DestinationSearch."""


class Dicomdata(DicomdataG):
    """Dicomdata."""


class Dictionary(DictionaryG):
    """Dictionary."""


class DictionaryAttach(DictionaryAttachG):
    """DictionaryAttach."""


class DictionaryEntry(DictionaryEntryG):
    """DictionaryEntry."""


class Drchrono(DrchronoG):
    """Drchrono."""


class Engine(EngineG):
    """Engine."""


class Filter(FilterG):
    """Filter."""


class FilterShare(FilterShareG):
    """FilterShare."""


class Group(GroupG):
    """Group."""


class Help(HelpG):
    """Help."""


class Hl7(Hl7G):
    """Hl7."""


class Hl7Accession(Hl7AccessionG):
    """Hl7Accession."""


class Hl7Template(Hl7TemplateG):
    """Hl7Template."""


class Hl7Transform(Hl7TransformG):
    """Hl7Transform."""


class Keyimage(KeyimageG):
    """Keyimage."""


class Link(LinkG):
    """Link."""


class LinkCharge(LinkChargeG):
    """LinkCharge."""


class LinkUsage(LinkUsageG):
    """LinkUsage."""


class Location(LocationG):
    """Location."""


class MailTemplate(MailTemplateG):
    """MailTemplate."""


class Meeting(MeetingG):
    """Meeting."""


class MeetingUser(MeetingUserG):
    """MeetingUser."""


class Message(MessageG):
    """Message."""


class Namespace(NamespaceG):
    """Namespace."""


class NamespaceChildren(NamespaceChildrenG):
    """NamespaceChildren."""


class Node(NodeG):
    """Node."""


class NodeConnect(NodeConnectG):
    """NodeConnect."""


class NodeEvent(NodeEventG):
    """NodeEvent."""


class NodeProgress(NodeProgressG):
    """NodeProgress."""


class NpiInviteShare(NpiInviteShareG):
    """NpiInviteShare."""


class Order(OrderG):
    """Order."""


class OrderSps(OrderSpsG):
    """OrderSps."""


class Patient(PatientG):
    """Patient."""


class Purge(PurgeG):
    """Purge."""


class Radreport(RadreportG):
    """Radreport."""


class RadreportAnalytics(RadreportAnalyticsG):
    """RadreportAnalytics."""


class RadreportTemplate(RadreportTemplateG):
    """RadreportTemplate."""


class Radreportmacro(RadreportmacroG):
    """Radreportmacro."""


class Role(RoleG):
    """Role."""


class Route(RouteG):
    """Route."""


class RouteRoundRobin(RouteRoundRobinG):
    """RouteRoundRobin."""


class RsnaclrDoc(RsnaclrDocG):
    """RsnaclrDoc."""


class RsnaclrSubset(RsnaclrSubsetG):
    """RsnaclrSubset."""


class Rsync(RsyncG):
    """Rsync."""


class Setting(SettingG):
    """Setting."""


class StorageStudy(StorageStudyG):
    """StorageStudy."""


class Study(StudyG):
    """Study."""


class StudyAnalytics(StudyAnalyticsG):
    """StudyAnalytics."""


class StudyAttachment(StudyAttachmentG):
    """StudyAttachment."""


class StudyCharge(StudyChargeG):
    """StudyCharge."""


class StudyComment(StudyCommentG):
    """StudyComment."""


class StudyDeleted(StudyDeletedG):
    """StudyDeleted."""


class StudyFetch(StudyFetchG):
    """StudyFetch."""


class StudyHl7(StudyHl7G):
    """StudyHl7."""


class StudyNotReady(StudyNotReadyG):
    """StudyNotReady."""


class StudyPhi(StudyPhiG):
    """StudyPhi."""


class StudyPush(StudyPushG):
    """StudyPush."""


class StudyPushStatus(StudyPushStatusG):
    """StudyPushStatus."""


class StudyQuestion(StudyQuestionG):
    """StudyQuestion."""


class StudyShare(StudyShareG):
    """StudyShare."""


class StudyShareAi(StudyShareAiG):
    """StudyShareAi."""


class StudyShareRsna(StudyShareRsnaG):
    """StudyShareRsna."""


class StudyStar(StudyStarG):
    """StudyStar."""


class StudyStatusLock(StudyStatusLockG):
    """StudyStatusLock."""


class StudyTiming(StudyTimingG):
    """StudyTiming."""


class System(SystemG):
    """System."""


class Tag(TagG):
    """Tag."""


class TagObject(TagObjectG):
    """TagObject."""


class TemplateAssign(TemplateAssignG):
    """TemplateAssign."""


class Terminology(TerminologyG):
    """Terminology."""


class TrainingAccount(TrainingAccountG):
    """TrainingAccount."""


class TrainingUser(TrainingUserG):
    """TrainingUser."""


class User(UserG):
    """User."""


class UserAccount(UserAccountG):
    """UserAccount."""


class UserAws(UserAwsG):
    """UserAws."""


class UserGroup(UserGroupG):
    """UserGroup."""


class UserInvite(UserInviteG):
    """UserInvite."""


class UserInviteShare(UserInviteShareG):
    """UserInviteShare."""


class UserLocation(UserLocationG):
    """UserLocation."""


class Validate(ValidateG):
    """Validate."""


class Webhook(WebhookG):
    """Webhook."""


class WebhookNode(WebhookNodeG):
    """WebhookNode."""


class WebhookOnce(WebhookOnceG):
    """WebhookOnce."""
