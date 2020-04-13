
class Accelerator(BaseModel):
    """Accelerator."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    account_id = Integer(description='FK. The associated account')
    account = Account(description='The associated account')
    address = String(description='The domain name and IP address')
    fqdn = String(description='The domain name and IP address')
    name = String(description='Name')
    push_shared_studies = Boolean(description='Push shared studies to the accelerator')
    serial_no = String(description='The serial number')
    upgrade = Boolean(description='Version and upgrade flag')
    version = String(description='Version and upgrade flag')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class Account(BaseModel):
    """Account."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    access_token = String(description='Stripe access token')
    billing = Dict(description='Billing information')
    can_request = Boolean(description='Can request')
    css = String(description='Account css')
    customfields = Dict(description='Custom fields')
    fair_warning = String(description='Fair warning data. This should be a JSON hash of the keys needed to run and distribute the report')
    name = String(description='Name')
    namespace_id = Integer(description='FK. Namespace of the account')
    namespace = Namespace(description='Namespace of the account')
    password_expire = Integer(description='Days before the passwords expire')
    role_id = Integer(description='FK. Default role id')
    role = Role(description='Default role id')
    saml = Dict(description='Native SAML information')
    session_expire = Integer(description='Minutes before an idle session expires')
    settings = Dict(description='Account settings')
    vanity_h = Dict(description='Vanity URLs')
    vendor = String(description='The vendor field')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class AccountCanShare(BaseModel):
    """AccountCanShare."""
    
    id = Integer(description='Primary key for internal use')
    account_id = Integer(description='FK. The account this rule is for')
    account = Account(description='The account this rule is for')
    by_account_id = Integer(description='FK. Who is sharing')
    by_account = Account(description='Who is sharing')
    by_group_id = Integer(description='FK. Who is sharing')
    by_group = Group(description='Who is sharing')
    by_location_id = Integer(description='FK. Who is sharing')
    by_location = Location(description='Who is sharing')
    by_user_id = Integer(description='FK. Who is sharing')
    by_user = User(description='Who is sharing')
    with_account_id = Integer(description='FK. With who can they share')
    with_account = Account(description='With who can they share')
    with_group_id = Integer(description='FK. With who can they share')
    with_group = Group(description='With who can they share')
    with_location_id = Integer(description='FK. With who can they share')
    with_location = Location(description='With who can they share')
    with_user_id = Integer(description='FK. With who can they share')
    with_user = User(description='With who can they share')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class AccountMd5Counter(BaseModel):
    """AccountMd5Counter."""
    
    id = Integer(description='Primary key for internal use')
    account_id = Integer(description='FK. Primary key for internal use')
    account = Account(description='Primary key for internal use')
    counter = Integer(description='Primary key for internal use')
    md5 = String(description='Primary key for internal use')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')


class AccountSamlRole(BaseModel):
    """AccountSamlRole."""
    
    id = Integer(description='Primary key for internal use')
    account_id = Integer(description='FK. The account this rule is for')
    account = Account(description='The account this rule is for')
    event_approve = Boolean(description='The event flags')
    event_harvest = Boolean(description='The event flags')
    event_link = Boolean(description='The event flags')
    event_link_mine = Boolean(description='The event flags')
    event_message = Boolean(description='The event flags')
    event_new_report = Boolean(description='The event flags')
    event_node = Boolean(description='The event flags')
    event_share = Boolean(description='The event flags')
    event_status_change = Boolean(description='The event flags')
    event_study_comment = Boolean(description='The event flags')
    event_thin_study_fail = Boolean(description='The event flags')
    event_thin_study_success = Boolean(description='The event flags')
    event_upload = Boolean(description='The event flags')
    event_upload_fail = Boolean(description='The event flags')
    namespace_id = Integer(description='FK. The namespace this is for')
    namespace = Namespace(description='The namespace this is for')
    role_id = Integer(description='FK. The role this is for')
    role = Role(description='The role this is for')
    saml_role = String(description='The SAML role')
    sequence = Integer(description='Ordering sequence')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class Activity(BaseModel):
    """Activity."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    message = String(description='Message associated with activity')
    namespace_id = Integer(description='FK. Id of the namespace the activity is associated with')
    namespace = Namespace(description='Id of the namespace the activity is associated with')
    study_id = Integer(description='FK. Id of the study the activity is associated with')
    study = Study(description='Id of the study the activity is associated with')
    type = String(description='Type of activity')
    user_id = Integer(description='FK. Id of the user the activity is specifically for.')
    user = User(description='Id of the user the activity is specifically for.')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class Analytics(BaseModel):
    """Analytics."""
    
    id = Integer(description='Primary key for internal use')
    last_id = Integer(description='The id of the last audit job processed')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class Annotation(BaseModel):
    """Annotation."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    frame_number = String(description='The frame identification')
    instance_uid = String(description='The frame identification')
    json = String(description='Data structure')
    series_uid = String(description='The frame identification')
    stamp = Boolean(description='This is a stamped so no other user can create or edit an annotation for this image')
    study_id = Integer(description='FK. Associated study')
    study = Study(description='Associated study')
    user_id = Integer(description='FK. User who created the annotation')
    user = User(description='User who created the annotation')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class Appointment(BaseModel):
    """Appointment."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    account_id = Integer(description='FK. The associated account')
    account = Account(description='The associated account')
    customfields = Dict(description='Custom fields')
    description = String(description='Description')
    end_time = DateTime(description='Time range')
    patient_id = Integer(description='FK. The associated patient')
    patient = Patient(description='The associated patient')
    start_time = DateTime(description='Time range')
    user_id = Integer(description='FK. The associated user')
    user = User(description='The associated user')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class ArchiveStudy(BaseModel):
    """ArchiveStudy."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    archive_vault_id = Integer(description='FK. The vault it is stored in')
    archive_vault = Archive(description='The vault it is stored in')
    datum_signature = String(description='Signature of the current study datum and phi')
    delay_until = DateTime(description='Delay the store or delete until this time')
    engine_id = Integer(description='FK. The storage engine')
    engine = Engine(description='The storage engine')
    job_id = String(description='When was the job started and the Last error message')
    last_error = String(description='When was the job started and the Last error message')
    need_delete = Boolean(description='Flag to control the store,restore and delete of the study. Indexed so the count in the control loop is fast')
    need_restore = Boolean(description='Flag to control the store,restore and delete of the study. Indexed so the count in the control loop is fast')
    need_store = Boolean(description='Flag to control the store,restore and delete of the study. Indexed so the count in the control loop is fast')
    phi_signature = String(description='Signature of the current study datum and phi')
    priority = Integer(description='Job priority. The higher the number the higher the priority of the job. This mirrors the archive flag in namespace')
    started_at = DateTime(description='When was the job started and the Last error message')
    storage_namespace = Integer(description='FK. The storage namespace')
    storage_namespace_obj = Namespace(description='The storage namespace')
    study_uid = String(description='Study instance id')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class ArchiveStudyAws(BaseModel):
    """ArchiveStudyAws."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    archive_study_id = Integer(description='FK. The associated study archive')
    archive_study = Archive(description='The associated study archive')
    aws_archive = String(description='The id of the AWS archive')
    aws_checksum = String(description='Checksum from AWS archive')
    aws_size = Integer(description='Checksum from AWS archive')
    datum_signature = String(description='Signature of the current study datum and phi')
    job_id = String(description='Job Id and state, restoring state can be PENDING, RETRIEVING, DONE')
    phi_signature = String(description='Signature of the current study datum and phi')
    state = String(description='Job Id and state, restoring state can be PENDING, RETRIEVING, DONE')
    type = String(description='Type archive either datum or phi')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class ArchiveVault(BaseModel):
    """ArchiveVault."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    closed = Boolean(description='Is the archive closed for new records')
    key = String(description='AWS credentials')
    region = String(description='AWS credentials')
    secret = String(description='AWS credentials')
    vault = String(description='AWS credentials')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class Audit(BaseModel):
    """Audit."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    account_id = Integer(description='FK. Account id of the association account')
    account = Account(description='Account id of the association account')
    action = String(description='The audit action')
    data = String(description='The audit data')
    parent_id = Integer(description='FK. Id of the parent object')
    parent = SelfField(description='Id of the parent object')
    pid = String(description='After the June 29 2016 release this holds the sid and client ip address')
    proxy_id = Integer(description='FK. Id of the proxy user who did the action')
    proxy = User(description='Id of the proxy user who did the action')
    type = String(description='Type of object we are auditing')
    user_id = Integer(description='FK. User who did the action')
    user = User(description='User who did the action')
    created = DateTime(description='Timestamp when the record was created')


class BillingSummary(BaseModel):
    """BillingSummary."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    account_id = Integer(description='FK. The account')
    account = Account(description='The account')
    account_name = String(description='The account')
    account_uuid = String(description='The account')
    admin_fee = Float(description='The fields')
    annual_volume_floor_count = Float(description='The fields')
    bucket_charges = Float(description='The fields')
    flat_rate = Float(description='The fields')
    month = String(description='The month this is for')
    monthly_volume_floor_count = Float(description='The fields')
    mtd_studies = Float(description='The fields')
    per_study_price = Float(description='The fields')
    size = Float(description='The fields')
    size_past = Float(description='The fields')
    size_price = Float(description='The fields')
    size_price_past = Float(description='The fields')
    storage_overage = Float(description='The fields')
    storage_price = Float(description='The fields')
    total = Float(description='The fields')
    total_storage_size = Float(description='The fields')
    ytd_studies = Float(description='The fields')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class BoxFile(BaseModel):
    """BoxFile."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    not_dicom = Boolean(description='Flag if this is not a dicom file')
    sha1 = String(description='Sha1 of the file')
    storage_namespace = Integer(description='FK. The storage namespace')
    storage_namespace_obj = Namespace(description='The storage namespace')
    study_uid = String(description='Study instance id')
    user_id = Integer(description='FK. User who created it')
    user = User(description='User who created it')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class Brand(BaseModel):
    """Brand."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    anonymous_permissions = String(description='The permissions over-ride as a json structure')
    cd_multi = String(description='The branding elements')
    cd_single = String(description='The branding elements')
    cd_viewer_settings = String(description='The branding elements')
    cluster_id = Integer(description='FK. The cluster associated with the brand')
    cluster = Cluster(description='The cluster associated with the brand')
    css = String(description='The branding elements')
    image_1 = String(description='The branding elements')
    image_2 = String(description='The branding elements')
    image_3 = String(description='The branding elements')
    less = String(description='The branding elements')
    name = String(description='Name for the brand')
    oauth = String(description='OAuth information')
    phr_default_events = String(description='The events over-ride as a json structure')
    phr_permissions = String(description='The permissions over-ride as a json structure')
    safari_instruction_1 = String(description='The branding elements')
    safari_instruction_2 = String(description='The branding elements')
    safari_instruction_3 = String(description='The branding elements')
    safari_instruction_4 = String(description='The branding elements')
    safari_instruction_5 = String(description='The branding elements')
    saml = Dict(description='Native SAML information')
    saml_redirect_url = String(description='PingOne SAML info')
    session_expire = Integer(description='Minutes before an idle session expires')
    settings = Dict(description='Brand settings')
    ssi_js = String(description='The branding elements')
    support_html = String(description='The branding elements')
    ui_json = String(description='The branding elements')
    uploader_icon = String(description='The branding elements')
    uploader_logo = String(description='The branding elements')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class BrandNamespace(BaseModel):
    """BrandNamespace."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    brand_id = Integer(description='FK. ')
    brand = Brand(description='')
    namespace_id = String(description='')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class BrandVanity(BaseModel):
    """BrandVanity."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    brand_id = Integer(description='FK. ')
    brand = Brand(description='')
    vanity = String(description='')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class Case(BaseModel):
    """Case."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    account_id = Integer(description='FK. The associated account')
    account = Account(description='The associated account')
    assigned_admin_date = DateTime(description='The admin assigned to the case')
    assigned_admin_id = Integer(description='FK. The admin assigned to the case')
    assigned_admin = User(description='The admin assigned to the case')
    assigned_medical_date = DateTime(description='The medical person assigned to the case')
    assigned_medical_id = Integer(description='FK. The medical person assigned to the case')
    assigned_medical = User(description='The medical person assigned to the case')
    case_status = String(description='The status of the case and the date of the last change')
    case_status_date = DateTime(description='The status of the case and the date of the last change')
    closed = Boolean(description='The case is closed')
    closed_date = DateTime(description='The case is closed')
    completed = Boolean(description='The case is completed')
    completed_date = DateTime(description='The case is completed')
    customfields = Dict(description='Custom fields')
    name = String(description='Basic information')
    namespace_id = Integer(description='FK. The namespace the case is in')
    namespace = Namespace(description='The namespace the case is in')
    returned_date = DateTime(description='The returned date and reason')
    returned_reason = String(description='The returned date and reason')
    study_charge_id = Integer(description='FK. Payment for the case')
    submitted = Boolean(description='The case is submitted')
    submitted_date = DateTime(description='The case is submitted')
    user_id = Integer(description='FK. The user the case is for')
    user = User(description='The user the case is for')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class CaseStatusLock(BaseModel):
    """CaseStatusLock."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    case_id = Integer(description='FK. The case and user id')
    case = Case(description='The case and user id')
    user_id = Integer(description='FK. The case and user id')
    user = User(description='The case and user id')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class CaseStudy(BaseModel):
    """CaseStudy."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    case_id = Integer(description='FK. ')
    case = Case(description='')
    storage_namespace = Integer(description='FK. ')
    storage_namespace_obj = Namespace(description='')
    study_uid = String(description='')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class Cluster(BaseModel):
    """Cluster."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    archive = Boolean(description='Is this an archive cluster')
    archive_cluster_id = Integer(description='FK. Id of the archive cluster this should be backed up to')
    archive_cluster = Archive(description='Id of the archive cluster this should be backed up to')
    backup_cluster_id = Integer(description='FK. Id of the backup cluster this should be backed up to')
    backup_cluster = Archive(description='Id of the backup cluster this should be backed up to')
    copies = Integer(description='Number of copies in the cluster')
    is_default = Boolean(description='This is the default cluster')
    max_days = Integer(description='Max days studies should stay in the cluster')
    name = String(description='Name for the cluster')
    rsync = Boolean(description='Is this a rsync cluster')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class ClusterAccount(BaseModel):
    """ClusterAccount."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    account_id = Integer(description='FK. Id of the cluster and account')
    account = Account(description='Id of the cluster and account')
    cluster_id = Integer(description='FK. Id of the cluster and account')
    cluster = Cluster(description='Id of the cluster and account')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class ClusterNamespace(BaseModel):
    """ClusterNamespace."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    cluster_id = Integer(description='FK. Id of the cluster and account')
    cluster = Cluster(description='Id of the cluster and account')
    namespace_id = Integer(description='FK. Id of the cluster and account')
    namespace = Namespace(description='Id of the cluster and account')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class Customcode(BaseModel):
    """Customcode."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    account_id = Integer(description='FK. The account')
    account = Account(description='The account')
    code = String(description='The code')
    has_zip = Boolean(description='Associated zip file')
    language = String(description='Type of code and the language')
    name = String(description='Basic information')
    settings = Json(description='The settings')
    type = String(description='Type of code and the language')
    zip = String(description='Associated zip file')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class CustomcodeDeploy(BaseModel):
    """CustomcodeDeploy."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    account_id = Integer(description='FK. Deployment information')
    account = Account(description='Deployment information')
    customcode_id = Integer(description='FK. Deployment information')
    customcode = Customcode(description='Deployment information')
    namespace_id = Integer(description='FK. Deployment information')
    namespace = Namespace(description='Deployment information')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class Customfield(BaseModel):
    """Customfield."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    account_id = Integer(description='FK. Associated object and account')
    account = Account(description='Associated object and account')
    capture_on_share_code = Boolean(description='Settings')
    dicom_tag = String(description='Map to this DICOM tag in storage')
    dicom_tag_ignore_empty = Boolean(description='Do not do the DICOM tag mapping if the field is empty')
    display_order = Integer(description='Order the fields should be displayed in')
    has_macro = Boolean(description='Flag if the values has a macro that needs expansion')
    hl7_component = Integer(description='HL7 options')
    hl7_field = Integer(description='HL7 options')
    hl7_segment = String(description='HL7 options')
    load_dicom_tag = Boolean(description='Load the DICOM tag from storage')
    load_from_sr = String(description='Load the value from the SR')
    load_hl7 = String(description='HL7 options')
    load_hl7_filter = String(description='HL7 options')
    name = String(description='Name and type  of the field')
    object = String(description='Associated object and account')
    options = String(description='Settings')
    other_dicom_tags = String(description='An array of other DICOM tags to map to in storage')
    required = Boolean(description='Settings')
    type = String(description='Name and type  of the field')
    wrapped_dicom_only = Boolean(description='Settings')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class DatabaseScripts(BaseModel):
    """DatabaseScripts."""
    
    id = Integer(description='Primary key for internal use')
    name = String(description='Name of the script that was run')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class Destination(BaseModel):
    """Destination."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    account_id = Integer(description='FK. The associated account')
    account = Account(description='The associated account')
    address = String(description='DICOM Address and port of the destination')
    aetitle = String(description='AEtitle')
    c_echo_interval = Integer(description='Do a c echo of the destination every c_echo_interval seconds')
    c_echo_schedule = String(description='The c echo schedule')
    can_query_retrieve = Boolean(description='Flags for destination capabilities')
    can_retrieve_thin = Boolean(description='Flags for destination capabilities')
    can_search = Boolean(description='Flags for destination capabilities')
    can_search_mwl = Boolean(description='Flags for destination capabilities')
    cd_burn_info = String(description='The CD burner information')
    cd_burn_name = String(description='The CD burner information')
    cd_burn_priority = Integer(description='The CD burner information')
    default_query_retrieve_level = String(description='How the query retrieve should be done')
    fire_webhooks = Boolean(description='Fire webhooks for this destination')
    gateway_settings = String(description='Gateway stores settings and data here')
    hl7_address = String(description='HL7 ORM destination address and port')
    hl7_fetch_filter = String(description='Fetch filter')
    hl7_port = Integer(description='HL7 ORM destination address and port')
    name = String(description='Name')
    node_id = Integer(description='FK. The associated node')
    node = Node(description='The associated node')
    path = String(description='Path for a FOLDER destination')
    port = Integer(description='DICOM Address and port of the destination')
    push_related_studies = Boolean(description='Push all related studies in the namespace when a study is pushed')
    sort_order = Integer(description='Sort order')
    sqlch_psh_if_img_unchg = Boolean(description='Flag if destination should squelch re-pushes if the image count has not changed')
    sqlch_psh_if_route_hl7 = Boolean(description='Flag if destination should squelch pushes that are generated by HL7 based routing')
    type = String(description='Type of destination can be either a DICOM, FOLDER, ACCELERATOR or BURNER')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class DestinationBurn(BaseModel):
    """DestinationBurn."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    batch_no = String(description='Batch no')
    destination_id = Integer(description='FK. The destination')
    destination = Destination(description='The destination')
    metrics = Dict(description='The metrics hash')
    node_id = Integer(description='FK. The node to use')
    node = Node(description='The node to use')
    patientid = String(description='The patient id')
    pickup = DateTime(description='When was this picked up by the node')
    status = String(description='Status of the delivery')
    study_h = Dict(description='The hash of studies to burn')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class DestinationSearch(BaseModel):
    """DestinationSearch."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    copy_to = Integer(description='FK. Namespace to copy any retrieved or thin studies into')
    copy_to_obj = Namespace(description='Namespace to copy any retrieved or thin studies into')
    count = Integer(description='Status of the search')
    create_study = Integer(description='Number of studies or thin studies to create from the search rather than creating an activity')
    create_thin = Integer(description='Number of studies or thin studies to create from the search rather than creating an activity')
    destination_id = Integer(description='FK. The destination to search')
    destination = Destination(description='The destination to search')
    extra = String(description='Extra data for speciality workflows like MPI')
    hl7_id = Integer(description='FK. The search was triggered by this HL7 message')
    hl7 = Hl7(description='The search was triggered by this HL7 message')
    node_id = Integer(description='FK. The node to use')
    node = Node(description='The node to use')
    payload = String(description='The search payload')
    pickup = DateTime(description='When was this picked up by the node')
    results = String(description='The search results')
    status = String(description='Status of the search')
    study_id = Integer(description='FK. Study id if this is a MWL search')
    study = Study(description='Study id if this is a MWL search')
    user_id = Integer(description='FK. The user who ran the search')
    user = User(description='The user who ran the search')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class Dicomdata(BaseModel):
    """Dicomdata."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    customfields = Dict(description='Custom fields')
    dicom_tags = Dict(description='The tags as a hstore')
    instance_uid = String(description='The series and image identification')
    phi_namespace = Integer(description='FK. Associated study')
    phi_namespace_obj = Namespace(description='Associated study')
    series_uid = String(description='The series and image identification')
    storage_namespace = Integer(description='FK. Associated study')
    storage_namespace_obj = Namespace(description='Associated study')
    study_id = Integer(description='FK. Associated study')
    study = Study(description='Associated study')
    study_uid = String(description='Associated study')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class Dictionary(BaseModel):
    """Dictionary."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    account_id = Integer(description='FK. Name and account')
    account = Account(description='Name and account')
    case_sensitive = Boolean(description='Settings')
    lookup = String(description='JSON array of the fields names to lookup on')
    name = String(description='Name and account')
    object = String(description='Type of object the dictionary runs against')
    replace = String(description='JSON array of the fields names to replace')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class DictionaryAttach(BaseModel):
    """DictionaryAttach."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    account_id = Integer(description='FK. The attachment is either to an account or a namespace')
    account = Account(description='The attachment is either to an account or a namespace')
    add_if_no_match = Boolean(description='Options')
    approve_if_match = Boolean(description='Options')
    dictionary_id = Integer(description='FK. Associated dictionary')
    dictionary = Dictionary(description='Associated dictionary')
    namespace_id = Integer(description='FK. The attachment is either to an account or a namespace')
    namespace = Namespace(description='The attachment is either to an account or a namespace')
    sequence = Integer(description='The sequence to order by')
    skip_if_lookup_unchanged = Boolean(description='Options')
    skip_if_replace_has_value = Boolean(description='Options')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class DictionaryEntry(BaseModel):
    """DictionaryEntry."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    dictionary_id = Integer(description='FK. Associated dictionary')
    dictionary = Dictionary(description='Associated dictionary')
    lookup = String(description='JSON array or regexp of the lookup value')
    md5 = String(description='MD5 of the record')
    regexp = Boolean(description='Is this a regexp')
    replace = String(description='JSON array of the replace values')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class Drchrono(BaseModel):
    """Drchrono."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    account_id = Integer(description='FK. Associated account')
    account = Account(description='Associated account')
    doctor = String(description='Doctor id on drchrono')
    refresh_token = String(description='Refresh token')
    user_id = Integer(description='FK. Associated user')
    user = User(description='Associated user')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class Engine(BaseModel):
    """Engine."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    cluster_id = Integer(description='FK. The cluster it is in')
    cluster = Cluster(description='The cluster it is in')
    fqdn = String(description='The fully qualified domain name of the storage engine')
    host_map = String(description='The host map JSON')
    idle_storage_host = String(description='The URL services should for archiving activity')
    is_full = Boolean(description='Flag if the engine is full or offline')
    is_offline = Boolean(description='Flag if the engine is full or offline')
    magic_sid = String(description='The magic sid for the storage engine')
    max_pull_jobs = Integer(description='The max number of pull jobs  to run on the engine at one time')
    max_push_jobs = Integer(description='The max number of push jobs to run on the engine at one time')
    no_phi = Boolean(description='No PHI is stored on this engine')
    no_purge = Boolean(description='Exclude studies on this engine from all purges')
    services_url = String(description='The URL services should use to access the storage engine')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class Filter(BaseModel):
    """Filter."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    account_id = Integer(description='FK. The associated account')
    account = Account(description='The associated account')
    configuration = String(description='The configuration as a json structure')
    name = String(description='Name')
    type = String(description='The type of the filter')
    user_id = Integer(description='FK. The user')
    user = User(description='The user')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class FilterShare(BaseModel):
    """FilterShare."""
    
    id = Integer(description='Primary key for internal use')
    account_id = Integer(description='FK. Who it is shared with')
    account = Account(description='Who it is shared with')
    filter_id = Integer(description='FK. Primary key for internal use')
    filter = Filter(description='Primary key for internal use')
    group_id = Integer(description='FK. Who it is shared with')
    group = Group(description='Who it is shared with')
    location_id = Integer(description='FK. Who it is shared with')
    location = Location(description='Who it is shared with')
    user_id = Integer(description='FK. Who it is shared with')
    user = User(description='Who it is shared with')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class Group(BaseModel):
    """Group."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    account_id = Integer(description='FK. The associated account')
    account = Account(description='The associated account')
    customfields = Dict(description='Custom fields')
    name = String(description='Name')
    namespace_id = Integer(description='FK. The namespace')
    namespace = Namespace(description='The namespace')
    role_id = Integer(description='FK. Default role id')
    role = Role(description='Default role id')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class Help(BaseModel):
    """Help."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    key = String(description='Help key')
    text = String(description='The help text')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class Hl7(BaseModel):
    """Hl7."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    accession_number_h = Dict(description='KV storage of all the accession numbers in the message')
    account_id = Integer(description='FK. Account the message is for')
    account = Account(description='Account the message is for')
    md5 = String(description='md5 hash of the message')
    message = String(description='The message data')
    node_id = Integer(description='FK. Node that sent the message')
    node = Node(description='Node that sent the message')
    patient_name = String(description='Patient Name')
    patientid = String(description='Patient MRN')
    type = String(description='Type of message')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class Hl7Accession(BaseModel):
    """Hl7Accession."""
    
    id = Integer(description='Primary key for internal use')
    accession_number = String(description='Accession number')
    account_id = Integer(description='FK. Account')
    account = Account(description='Account')
    hl7_id = Integer(description='FK. Message')
    hl7 = Hl7(description='Message')
    study_id = Integer(description='FK. Id of the study an order was associated with by the /study/find/order functionality')
    study = Study(description='Id of the study an order was associated with by the /study/find/order functionality')
    type = String(description='Type of message')
    created = DateTime(description='Timestamp when the record was created')


class Hl7Template(BaseModel):
    """Hl7Template."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    account_id = Integer(description='FK. The associated account')
    account = Account(description='The associated account')
    body = String(description='Type of message')
    name = String(description='Name')
    type = String(description='Type of message')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class Hl7Transform(BaseModel):
    """Hl7Transform."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    account_id = Integer(description='FK. The associated account')
    account = Account(description='The associated account')
    conditions = String(description='')
    name = String(description='Name')
    order_by = Integer(description='')
    replacements = String(description='')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class Keyimage(BaseModel):
    """Keyimage."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    frame_number = String(description='The frame identification')
    instance_uid = String(description='The frame identification')
    series_uid = String(description='The frame identification')
    study_id = Integer(description='FK. Associated study')
    study = Study(description='Associated study')
    user_id = Integer(description='FK. User who created the annotation')
    user = User(description='User who created the annotation')
    version = String(description='The frame identification')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class Link(BaseModel):
    """Link."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    acceptance_required = Boolean(description='Is acceptance of the study required')
    account_id = Integer(description='FK. The associated account')
    account = Account(description='The associated account')
    action = String(description='Action to take on the link. This can either be view, list or upload')
    anonymize = String(description='Anonymization rules to be applied to studies uploaded via this link')
    charge_amount = Integer(description='Charge amount in pennies')
    charge_currency = String(description='Charge amount in pennies')
    charge_description = String(description='Charge amount in pennies')
    email = String(description='Email address, any additional message and other notification emails to send the link to')
    filter = String(description='The study the link is for or the filter expression or the namespace for an upload action')
    include_priors = Boolean(description='Include priors')
    max_hits = Integer(description='The maximum number of times the link can be used')
    message = String(description='Email address, any additional message and other notification emails to send the link to')
    minutes_alive = Integer(description='The number of minutes the link will be alive for')
    namespace_id = Integer(description='FK. The study the link is for or the filter expression or the namespace for an upload action')
    namespace = Namespace(description='The study the link is for or the filter expression or the namespace for an upload action')
    notify = String(description='Email address, any additional message and other notification emails to send the link to')
    parameters = String(description='Optional parameter to include on the link')
    password = String(description='Password to access link')
    password_is_dob = Boolean(description='The password is the study DOB')
    password_max_attempts = Integer(description='Max number of failed password attempts on the link')
    pin_auth = Boolean(description='The email must be an account member and PIN auth is required')
    prompt_for_anonymize = Boolean(description='Anonymization rules to be applied to studies uploaded via this link')
    referer = String(description='The referer for the link')
    share_code = String(description='Share code for the link')
    share_on_view = Boolean(description='Share the study after it is viewed')
    skip_email_prompt = Boolean(description='Skip ask for the email')
    study_id = Integer(description='FK. The study the link is for or the filter expression or the namespace for an upload action')
    study = Study(description='The study the link is for or the filter expression or the namespace for an upload action')
    upload_match = String(description='Must match rules for uploads')
    use_share_code = Boolean(description='Use the namespace share code information for uploads')
    user_id = Integer(description='FK. The user who created the link. Any filter is applied in this users context as well')
    user = User(description='The user who created the link. Any filter is applied in this users context as well')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class LinkCharge(BaseModel):
    """LinkCharge."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    account_id = Integer(description='FK. Link and account id')
    account = Account(description='Link and account id')
    charge_amount = Integer(description='The charge amount')
    link_id = Integer(description='FK. Link and account id')
    link = Link(description='Link and account id')
    processor = String(description='The processor information')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class LinkUsage(BaseModel):
    """LinkUsage."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    account_id = Integer(description='FK. Link and account id')
    account = Account(description='Link and account id')
    client_address = String(description='Address that used the link')
    client_email = String(description='Address that used the link')
    extra = String(description='Any extra analytical data to store with the link')
    link_id = Integer(description='FK. Link and account id')
    link = Link(description='Link and account id')
    sid = String(description='Sid of the session')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class Location(BaseModel):
    """Location."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    account_id = Integer(description='FK. The associated account')
    account = Account(description='The associated account')
    customfields = Dict(description='Custom fields')
    name = String(description='Name')
    namespace_id = Integer(description='FK. The namespace')
    namespace = Namespace(description='The namespace')
    role_id = Integer(description='FK. Default role id')
    role = Role(description='Default role id')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class MailTemplate(BaseModel):
    """MailTemplate."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    account_id = Integer(description='FK. Account the template is for')
    account = Account(description='Account the template is for')
    bcc = String(description='Email addresses')
    cc = String(description='Email addresses')
    delay = Integer(description='Number of seconds to delay sending the mail for')
    filter_field = String(description='Filter field and regexp')
    filter_regexp = String(description='Filter field and regexp')
    from_email_address = String(description='Email addresses')
    from_email_name = String(description='Email addresses')
    html = String(description='Templates')
    namespace_id = Integer(description='FK. Scope it down to a namespace or vanity')
    namespace = Namespace(description='Scope it down to a namespace or vanity')
    reply_to_email_address = String(description='Email addresses')
    sms = String(description='Templates')
    txt = String(description='Templates')
    type = String(description='Tmpl type')
    vanity = String(description='Scope it down to a namespace or vanity')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class Meeting(BaseModel):
    """Meeting."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    link_id = Integer(description='FK. Associated link')
    link = Link(description='Associated link')
    name = String(description='Name of the meeting')
    state = String(description='Current state data structure')
    study_id = Integer(description='FK. Associated study')
    study = Study(description='Associated study')
    user_id = Integer(description='FK. User who created the meeting')
    user = User(description='User who created the meeting')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class MeetingUser(BaseModel):
    """MeetingUser."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    meeting_id = Integer(description='FK. ')
    meeting = Meeting(description='')
    user_id = Integer(description='FK. ')
    user = User(description='')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class Message(BaseModel):
    """Message."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    body = String(description='Body of the message')
    namespace_id = Integer(description='FK. The namespace the message is for')
    namespace = Namespace(description='The namespace the message is for')
    subject = String(description='Subject')
    user_id = Integer(description='FK. The user who sent the message')
    user = User(description='The user who sent the message')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class Namespace(BaseModel):
    """Namespace."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    account_id = Integer(description='FK. Who it is linked to')
    account = Account(description='Who it is linked to')
    anonymize = String(description='Anonymization rules')
    archive = Integer(description='Archive setting. 0 = no archive or else archive and restore based on the priority value of the setting. e.g. 99 is high priority, -99 is low priority')
    cache = Boolean(description='Cache new studies image')
    charge_description = String(description='Charging information')
    coverpage = String(description='Cover page template')
    currency = String(description='Charging information')
    event_approve = Boolean(description='The default event settings flags')
    event_harvest = Boolean(description='The default event settings flags')
    event_link = Boolean(description='The default event settings flags')
    event_link_mine = Boolean(description='The default event settings flags')
    event_message = Boolean(description='The default event settings flags')
    event_new_report = Boolean(description='The default event settings flags')
    event_node = Boolean(description='The default event settings flags')
    event_share = Boolean(description='The default event settings flags')
    event_status_change = Boolean(description='The default event settings flags')
    event_study_comment = Boolean(description='The default event settings flags')
    event_thin_study_fail = Boolean(description='The default event settings flags')
    event_thin_study_success = Boolean(description='The default event settings flags')
    event_upload = Boolean(description='The default event settings flags')
    event_upload_fail = Boolean(description='The default event settings flags')
    group_id = Integer(description='FK. Who it is linked to')
    group = Group(description='Who it is linked to')
    harvest_hold = Integer(description='Storage settings')
    hl7_template = String(description='HL7 template for the namespace')
    linkage_name = String(description='Name of the linked object for sorting purposes')
    location_id = Integer(description='FK. Who it is linked to')
    location = Location(description='Who it is linked to')
    must_approve = Boolean(description='Flag if study approval for a share is needed')
    must_approve_upload = Boolean(description='Flag if study approval for a upload is needed')
    no_cluster_archive = Boolean(description='Storage settings')
    no_share = Boolean(description='Flag if this namespace can not be shared into')
    prompt_for_anonymize = Boolean(description='Anonymization rules')
    search_threshold = Integer(description='The UI search threshold')
    second_opinion_config = String(description='Second opinion settings')
    second_opinion_share = Boolean(description='Second opinion settings')
    settings = Dict(description='Namespace settings')
    share_code = String(description='Share code for the name space')
    share_description = String(description='Share code for the name space')
    share_pricing = String(description='Charging information')
    share_settings = String(description='Share code for the name space')
    share_via_gateway = Boolean(description='Allow gateway uploads to the share code')
    study_defaults = String(description='Study defaults')
    upload_hold = Integer(description='Storage settings')
    user_id = Integer(description='FK. Who it is linked to')
    user = User(description='Who it is linked to')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class NamespaceChildren(BaseModel):
    """NamespaceChildren."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    account_id = Integer(description='FK. Account the namespaces are in')
    account = Account(description='Account the namespaces are in')
    child_id = Integer(description='FK. Child namespace')
    child = SelfField(description='Child namespace')
    fields = String(description='JSON list of the fields')
    namespace_id = Integer(description='FK. Parent namespace')
    namespace = Namespace(description='Parent namespace')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class Node(BaseModel):
    """Node."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    accelerator_id = Integer(description='FK. The associated accelerator')
    accelerator = Accelerator(description='The associated accelerator')
    account_id = Integer(description='FK. The associated account')
    account = Account(description='The associated account')
    category = String(description='Category and searchability')
    configuration_h = Dict(description='The configuration hash')
    ctc_bucket = String(description='Category and searchability')
    facility_contact = String(description='Facility information')
    facility_contact_title = String(description='Facility information')
    facility_email = String(description='Facility information')
    facility_name = String(description='Facility information')
    facility_notes = String(description='Facility information')
    facility_state = String(description='Facility information')
    facility_zip = String(description='Facility information')
    is_public = Boolean(description='Category and searchability')
    monitor_email = String(description='Monitoring flags')
    monitor_node_last_send = Boolean(description='Monitoring flags')
    monitor_node_last_send_threshold = Integer(description='Number of minutes as the threshold for firing the notification')
    monitor_node_ping = Boolean(description='Monitoring flags')
    monitor_node_slow_push = Boolean(description='Monitoring flags')
    monitor_node_slow_push_threshold = Integer(description='Number of minutes as the threshold for firing the notification')
    monitor_study_create = Boolean(description='Monitoring flags')
    monitor_study_create_threshold = Integer(description='Number of minutes as the threshold for firing the notification')
    name = String(description='Name')
    namespace_id = Integer(description='FK. The associated namespace')
    namespace = Namespace(description='The associated namespace')
    reload_configuration = Boolean(description='Reload configuration')
    serial_no = String(description='The serial number')
    settings = Dict(description='Account settings overrides')
    type = String(description='The type of the node')
    user_id = Integer(description='FK. The user to generate a node sid for')
    user = User(description='The user to generate a node sid for')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class NodeConnect(BaseModel):
    """NodeConnect."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    from_account_id = Integer(description='FK. Node information')
    from_account = Account(description='Node information')
    message = String(description='Message')
    node_id = Integer(description='FK. Node information')
    node = Node(description='Node information')
    to_account_id = Integer(description='FK. Node information')
    to_account = Account(description='Node information')
    user_id = Integer(description='FK. Node information')
    user = User(description='Node information')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')


class NodeEvent(BaseModel):
    """NodeEvent."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    count = Integer(description='Count of the number of times this event was fired. The audit table will have detail on the individual events.')
    destination_id = Integer(description='FK. The event parameters')
    destination = Destination(description='The event parameters')
    event = String(description='The event parameters')
    node_id = Integer(description='FK. The event parameters')
    node = Node(description='The event parameters')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class NodeProgress(BaseModel):
    """NodeProgress."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    accession_number = String(description='Study information')
    destination_id = Integer(description='FK. Node information')
    destination = Destination(description='Node information')
    detail = String(description='Description of the progress')
    node_id = Integer(description='FK. Node information')
    node = Node(description='Node information')
    patientid = String(description='Study information')
    queue = String(description='Queue information')
    state = String(description='Queue information')
    study_uid = String(description='Study information')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')


class NpiInviteShare(BaseModel):
    """NpiInviteShare."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    done = Boolean(description='Flag if the share was done')
    message = String(description='Share message')
    npi = String(description='NPI to invite')
    study_id = Integer(description='FK. Id for the study to be shared')
    study = Study(description='Id for the study to be shared')
    user_id = Integer(description='FK. Id the invitation is from')
    user = User(description='Id the invitation is from')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class Order(BaseModel):
    """Order."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    accession_number = String(description='Basic information')
    account_id = Integer(description='FK. The associated account')
    account = Account(description='The associated account')
    customfields = Dict(description='Custom fields')
    order_number = String(description='Basic information')
    patient_birth_date = String(description='Basic information')
    patient_name = String(description='Basic information')
    patient_sex = String(description='Basic information')
    patientid = String(description='Basic information')
    referring_physician = String(description='Basic information')
    sending_facility = String(description='Basic information')
    study_uid = String(description='The study uid')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class OrderSps(BaseModel):
    """OrderSps."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    modality = String(description='The step information')
    mpps_status = String(description='The mpps information')
    mpps_uid = String(description='The mpps information')
    order_id = Integer(description='FK. The associated order')
    order = Order(description='The associated order')
    requested_procedure_description = String(description='The step information')
    requested_procedure_id = String(description='The step information')
    scheduled_procedure_step_description = String(description='The step information')
    scheduled_procedure_step_id = String(description='The step information')
    scheduled_procedure_step_start_date = String(description='The step information')
    scheduled_procedure_step_start_time = String(description='The step information')
    scheduled_station_aetitle = String(description='The step information')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class Patient(BaseModel):
    """Patient."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    account_id = Integer(description='FK. The associated account')
    account = Account(description='The associated account')
    alt_email = String(description='Contact info')
    alt_mobile_phone = String(description='Contact info')
    birth_date = String(description='Basic information')
    customfields = Dict(description='Custom fields')
    email = String(description='Contact info')
    event_share = Boolean(description='The event flags')
    first = String(description='Basic information')
    last = String(description='Basic information')
    last_event = DateTime(description='Ordering field')
    mobile_phone = String(description='Contact info')
    mrn = String(description='Basic information')
    name = String(description='Basic information')
    sex = String(description='Basic information')
    user_id = Integer(description='FK. The associated user')
    user = User(description='The associated user')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class Purge(BaseModel):
    """Purge."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    account_id = Integer(description='FK. The associated account')
    account = Account(description='The associated account')
    adults = Boolean(description='Include adults  in this rule')
    archive = Boolean(description='Flag to make it a thin, archive or skinny study')
    days_old = Integer(description='Age of the studies to purge and how to calculate the purge')
    days_old_how = String(description='Age of the studies to purge and how to calculate the purge')
    global = Boolean(description='Is this a global purge rule')
    max_deletes = Integer(description='Maximum number of purges per run of the rule')
    minors = Boolean(description='Include minors in this rule')
    modalities = String(description='The modalities to limit the rule to as a JSON array')
    name = String(description='Name')
    namespaces = String(description='The namespaces to limit the rule to as a JSON array')
    owned_phr = Boolean(description='Include owned PHR namespaces in the rule')
    shared_from_phr = Boolean(description='If a study was shared from a PHR delete the copy in the PHR as well')
    skinny = Boolean(description='Flag to make it a thin, archive or skinny study')
    study_status_tags = String(description='A CSV list of the study status tags limit the purge to')
    suspended = Boolean(description='Suspend this rule from running')
    thin = Boolean(description='Flag to make it a thin, archive or skinny study')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class Radreport(BaseModel):
    """Radreport."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    attachment = String(description='The attachment information')
    fields = String(description='The fields in the report')
    study_id = Integer(description='FK. Attached study')
    study = Study(description='Attached study')
    type = String(description='Type of report')
    user_id = Integer(description='FK. User who created the report')
    user = User(description='User who created the report')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class RadreportAnalytics(BaseModel):
    """RadreportAnalytics."""
    
    id = Integer(description='Primary key for internal use')
    account_id = Integer(description='FK. The primary keys')
    account = Account(description='The primary keys')
    day = Date(description='The day')
    namespace_id = Integer(description='FK. The primary keys')
    namespace = Namespace(description='The primary keys')
    radreport_create = Integer(description='The metrics')
    radreport_delete = Integer(description='The metrics')
    radreport_report_generated = Integer(description='The metrics')
    radreport_signed = Integer(description='The metrics')
    user_id = Integer(description='FK. The primary keys')
    user = User(description='The primary keys')


class RadreportTemplate(BaseModel):
    """RadreportTemplate."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    account_id = Integer(description='FK. Associated account')
    account = Account(description='Associated account')
    active = Boolean(description='Is this the active record')
    body = String(description='Template fields')
    name = String(description='Description of report template')
    options = String(description='Template metadata')
    preview = String(description='Template fields')
    type = String(description='Type of report template')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class Radreportmacro(BaseModel):
    """Radreportmacro."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    account_id = Integer(description='FK. Associated account')
    account = Account(description='Associated account')
    body = String(description='Macro fields')
    hotkey = String(description='Macro fields')
    modality = String(description='Macro fields')
    name = String(description='Macro fields')
    type = String(description='Type of report')
    user_id = Integer(description='FK. User who owns the macro')
    user = User(description='User who owns the macro')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class Role(BaseModel):
    """Role."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    account_id = Integer(description='FK. The associated account')
    account = Account(description='The associated account')
    description = String(description='Description')
    name = String(description='Name')
    permissions = String(description='The permissions as a json structure')
    type = String(description='Type if role is system created')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class Route(BaseModel):
    """Route."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    account_id = Integer(description='FK. The associated account')
    account = Account(description='The associated account')
    actions = String(description='The rule actions')
    conditions = String(description='The rule conditions')
    delay = Integer(description='Number of minutes to delay running this rule after it is triggered')
    delay_till_schedule = Boolean(description='Delay running the rule until the schedule time')
    manual_roles = Dict(description='Roles that can manually run this route')
    name = String(description='Name')
    namespace_id = Integer(description='FK. The associated namespace')
    namespace = Namespace(description='The associated namespace')
    no_re_run = Boolean(description='Should the rule be not be run on a re-run of a storage notification')
    on_harvest = Boolean(description='Should the rule be run on harvested studies')
    on_manual_route = Boolean(description='Should the rule be able to be applied manually')
    on_share = Boolean(description='Should the rule be run on shared studies')
    on_thin = Boolean(description='Should the rule be run on the creation of thin studies')
    on_upload = Boolean(description='Should the rule be run on uploaded studies')
    options = String(description='The rule options')
    other_namespaces = Dict(description='The other namespaces this rule is associated with')
    schedule = String(description='The rule schedule')
    suspended = Boolean(description='Suspend this rule from running')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class RouteRoundRobin(BaseModel):
    """RouteRoundRobin."""
    
    id = Integer(description='Primary key for internal use')
    action = String(description='Primary key for internal use')
    route_id = Integer(description='FK. Primary key for internal use')
    route = Route(description='Primary key for internal use')
    study_id = Integer(description='FK. Primary key for internal use')
    study = Study(description='Primary key for internal use')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class RsnaclrDoc(BaseModel):
    """RsnaclrDoc."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    attachmentid = String(description='')
    author = Json(description='')
    class_code = Json(description='')
    comments = String(description='')
    communityid = String(description='')
    confidentiality_code = Json(description='')
    creation_time = String(description='')
    documentid = String(description='')
    event_code_list = Json(description='')
    format_code = Json(description='')
    healthcare_facility_type_code = Json(description='')
    language_code = String(description='')
    legal_authenticator = String(description='')
    limited_metadata = Boolean(description='')
    mime_type = String(description='')
    patientid = String(description='')
    practice_setting_code = Json(description='')
    reference_id_list = Json(description='')
    repositoryid = String(description='')
    rsna_status = String(description='')
    rsnaclr_subset_id = Integer(description='FK. The associated submission set')
    rsnaclr_subset = RsnaclrSubset(description='The associated submission set')
    service_start_time = String(description='')
    service_stop_time = String(description='')
    sha1 = String(description='')
    size = Integer(description='')
    source_patient_id = String(description='')
    source_patient_info = Json(description='')
    title = String(description='')
    type_code = Json(description='')
    uniqueid = String(description='')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class RsnaclrSubset(BaseModel):
    """RsnaclrSubset."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    author = Json(description='')
    comments = String(description='')
    communityid = String(description='')
    content_type_code = Json(description='')
    intended_recipient = Json(description='')
    limited_metadata = Boolean(description='')
    patientid = String(description='RSNA patient Id')
    rsna_status = String(description='Status of the submission set')
    sourceid = String(description='')
    study_id = Integer(description='FK. Study the submission set is attached to')
    study = Study(description='Study the submission set is attached to')
    submission_time = String(description='')
    title = String(description='')
    uniqueid = String(description='')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class Rsync(BaseModel):
    """Rsync."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    is_full = Boolean(description='Is the account full')
    name = String(description='ssh account name')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class Setting(BaseModel):
    """Setting."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    key = String(description='')
    user_id = Integer(description='FK. ')
    user = User(description='')
    value = String(description='')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class StorageStudy(BaseModel):
    """StorageStudy."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    corrupt = Boolean(description='Flag if the study is corrupt')
    engine_id = Integer(description='FK. The storage engine')
    engine = Engine(description='The storage engine')
    is_frozen = Boolean(description='Flag if the study is frozen')
    last_update = DateTime(description='Time of the last update of the study')
    rsync_id = Integer(description='FK. The rysnc account')
    rsync = Rsync(description='The rysnc account')
    storage_namespace = Integer(description='FK. The storage namespace')
    storage_namespace_obj = Namespace(description='The storage namespace')
    study_uid = String(description='Study instance id')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class Study(BaseModel):
    """Study."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    accession_number = String(description='This is the MRN')
    attachment_count = Integer(description='This is the MRN')
    callback_url = String(description='2013-11 - This is depreciated as the storage id is now used. If this is dropped update its usage in the database script.')
    compressed_size = Integer(description='This is the MRN')
    customfields = Dict(description='Custom fields')
    destination_ae_title = String(description='The aetitle the study was harvested against')
    engine_id = Integer(description='FK. The storage engine the study is stored on')
    engine = Engine(description='The storage engine the study is stored on')
    image_count = Integer(description='This is the MRN')
    integration_key = String(description='Key for integration with third party systems')
    medical_record_locator = String(description='This is the MRN')
    modality = String(description='This is the MRN')
    must_approve = Boolean(description='Flag if study approval is needed')
    node_id = Integer(description='FK. The harvest node id')
    node = Node(description='The harvest node id')
    patient_additional_history = String(description='This is the MRN')
    patient_address = String(description='This is the MRN')
    patient_age = String(description='This is the MRN')
    patient_birth_date = String(description='This is the MRN')
    patient_birth_time = String(description='This is the MRN')
    patient_birthname = String(description='This is the MRN')
    patient_comments = String(description='This is the MRN')
    patient_current_location = String(description='This is the MRN')
    patient_ethnic_group = String(description='This is the MRN')
    patient_institution_residence = String(description='This is the MRN')
    patient_mother_birthname = String(description='This is the MRN')
    patient_name = String(description='Dicom fields')
    patient_name_other = String(description='This is the MRN')
    patient_occupation = String(description='This is the MRN')
    patient_phone = String(description='This is the MRN')
    patient_religious_preference = String(description='This is the MRN')
    patient_sex = String(description='This is the MRN')
    patient_size = String(description='This is the MRN')
    patient_weight = String(description='This is the MRN')
    patientid = String(description='This is the MRN')
    patientid_other = String(description='This is the MRN')
    phantom = Boolean(description='A phantom study is one that is in the process loading into storage')
    phi_namespace = Integer(description='FK. The PHI namespace. This controls the study visibility')
    phi_namespace_obj = Namespace(description='The PHI namespace. This controls the study visibility')
    referring_physician = String(description='This is the MRN')
    shared_from = Integer(description='FK. Id of the study this was originally shared from')
    shared_from_obj = StudyShare(description='Id of the study this was originally shared from')
    size = Integer(description='This is the MRN')
    source = String(description='The original source of the study')
    source_ae_title = String(description='The aetitle the study was harvested against')
    storage_namespace = Integer(description='FK. The storage namespace')
    storage_namespace_obj = Namespace(description='The storage namespace')
    storage_state = String(description='Storage state. Empty or null is available or else &#39;U&#39; if unavailable or &#39;R&#39; if getting restored from the archive')
    study_date = String(description='This is the MRN')
    study_description = String(description='This is the MRN')
    study_status = String(description='The status of the study')
    study_time = String(description='This is the MRN')
    study_uid = String(description='Study instance id')
    thin = Boolean(description='A thin study is not in primary storage and needs to be query retrieved to be loaded into storage or loaded from an archive')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class StudyAnalytics(BaseModel):
    """StudyAnalytics."""
    
    id = Integer(description='Primary key for internal use')
    account_id = Integer(description='FK. The primary keys')
    account = Account(description='The primary keys')
    day = Date(description='The day')
    login = Integer(description='Login')
    namespace_id = Integer(description='FK. The primary keys')
    namespace = Namespace(description='The primary keys')
    study_approve = Integer(description='Study approved')
    study_auto_approve = Integer(description='Study approved')
    study_create = Integer(description='Total study created')
    study_create_copy = Integer(description='Count by creation type')
    study_create_harvest = Integer(description='Count by creation type')
    study_create_share = Integer(description='Count by creation type')
    study_create_upload = Integer(description='Count by creation type')
    study_delete = Integer(description='Delete, view download and push')
    study_download = Integer(description='Delete, view download and push')
    study_push = Integer(description='Delete, view download and push')
    study_report_view = Integer(description='Delete, view download and push')
    study_share_in = Integer(description='Share in and out')
    study_share_out = Integer(description='Share in and out')
    study_view = Integer(description='Delete, view download and push')


class StudyAttachment(BaseModel):
    """StudyAttachment."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    attachment_guid = String(description='The attachment id')
    storage_namespace = Integer(description='FK. The storage namespace')
    storage_namespace_obj = Namespace(description='The storage namespace')
    study_uid = String(description='Study instance id')
    user_id = Integer(description='FK. The user id')
    user = User(description='The user id')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class StudyCharge(BaseModel):
    """StudyCharge."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    account_id = Integer(description='FK. The study and account id')
    account = Account(description='The study and account id')
    detail = String(description='The stripe capture')
    study_id = Integer(description='FK. The study and account id')
    study = Study(description='The study and account id')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class StudyComment(BaseModel):
    """StudyComment."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    body = String(description='Body of the comment')
    study_id = Integer(description='FK. The study and user id')
    study = Study(description='The study and user id')
    user_id = Integer(description='FK. The study and user id')
    user = User(description='The study and user id')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class StudyDeleted(BaseModel):
    """StudyDeleted."""
    
    id = Integer(description='')
    uuid = String(description='')
    accession_number = String(description='')
    attachment_count = Integer(description='')
    callback_url = String(description='')
    compressed_size = Integer(description='')
    customfields = Dict(description='')
    deleted = DateTime(description='')
    deleted_by = Integer(description='FK. ')
    deleted_by_obj = User(description='')
    destination_ae_title = String(description='')
    engine_id = Integer(description='FK. ')
    engine = Engine(description='')
    image_count = Integer(description='')
    integration_key = String(description='')
    medical_record_locator = String(description='')
    modality = String(description='')
    must_approve = Boolean(description='')
    node_id = Integer(description='FK. ')
    node = Node(description='')
    patient_additional_history = String(description='')
    patient_address = String(description='')
    patient_age = String(description='')
    patient_birth_date = String(description='')
    patient_birth_time = String(description='')
    patient_birthname = String(description='')
    patient_comments = String(description='')
    patient_current_location = String(description='')
    patient_ethnic_group = String(description='')
    patient_institution_residence = String(description='')
    patient_mother_birthname = String(description='')
    patient_name = String(description='')
    patient_name_other = String(description='')
    patient_occupation = String(description='')
    patient_phone = String(description='')
    patient_religious_preference = String(description='')
    patient_sex = String(description='')
    patient_size = String(description='')
    patient_weight = String(description='')
    patientid = String(description='')
    patientid_other = String(description='')
    phantom = Boolean(description='')
    phi_namespace = Integer(description='FK. ')
    phi_namespace_obj = Namespace(description='')
    referring_physician = String(description='')
    shared_from = Integer(description='FK. ')
    shared_from_obj = StudyShare(description='')
    size = Integer(description='')
    source = String(description='')
    source_ae_title = String(description='')
    storage_namespace = Integer(description='FK. ')
    storage_namespace_obj = Namespace(description='')
    storage_state = String(description='')
    study_date = String(description='')
    study_description = String(description='')
    study_status = String(description='')
    study_time = String(description='')
    study_uid = String(description='')
    thin = Boolean(description='')
    created = DateTime(description='')
    created_by = Integer(description='FK. ')
    created_by_obj = User(description='')
    updated = DateTime(description='')
    updated_by = Integer(description='FK. ')
    updated_by_obj = User(description='')


class StudyFetch(BaseModel):
    """StudyFetch."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    accession_number = String(description='The accession number to fetch')
    destination_id = Integer(description='FK. The destination')
    destination = Destination(description='The destination')
    node_id = Integer(description='FK. The node to use')
    node = Node(description='The node to use')
    patientid = String(description='Extra data to scope the fetch down further')
    pickup = DateTime(description='When was this picked up by the node')
    source = String(description='How was the study fetch trigger, &#39;H&#39;l7 or &#39;O&#39;ther')
    status = String(description='Status of the delivery')
    study_id = Integer(description='FK. Study id if this is for a thin study')
    study = Study(description='Study id if this is for a thin study')
    study_uid = String(description='Extra data to scope the fetch down further')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class StudyHl7(BaseModel):
    """StudyHl7."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    ack = String(description='The returned ACK message')
    destination_id = Integer(description='FK. The destination')
    destination = Destination(description='The destination')
    hl7_id = Integer(description='FK. The study or hl7 id to use')
    hl7 = Hl7(description='The study or hl7 id to use')
    hl7_template_hl7_id = Integer(description='FK. HL7 template and associated hl7 message to use in the template')
    hl7_template_hl7 = Hl7Template(description='HL7 template and associated hl7 message to use in the template')
    hl7_template_id = Integer(description='FK. HL7 template and associated hl7 message to use in the template')
    hl7_template = Hl7Template(description='HL7 template and associated hl7 message to use in the template')
    node_id = Integer(description='FK. The node to use')
    node = Node(description='The node to use')
    pickup = DateTime(description='When was this picked up by the node')
    status = String(description='Status of the delivery')
    study_id = Integer(description='FK. The study or hl7 id to use')
    study = Study(description='The study or hl7 id to use')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class StudyNotReady(BaseModel):
    """StudyNotReady."""
    
    id = Integer(description='Primary key for internal use')
    phi_namespace = Integer(description='FK. Primary key for internal use')
    phi_namespace_obj = Namespace(description='Primary key for internal use')
    study_id = Integer(description='FK. Primary key for internal use')
    study = Study(description='Primary key for internal use')


class StudyPhi(BaseModel):
    """StudyPhi."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    customfields = Dict(description='The PHI override in DICOM tag=&gt;value format. We name this customfields so we get the merging at save')
    extended = String(description='The extended PHI attributes')
    study_id = Integer(description='FK. The study id')
    study = Study(description='The study id')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class StudyPush(BaseModel):
    """StudyPush."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    destination_id = Integer(description='FK. The destination')
    destination = Destination(description='The destination')
    detail = String(description='Additional detail to send to the node')
    image_count = Integer(description='The image count when the study was pushed')
    node_id = Integer(description='FK. The node to use')
    node = Node(description='The node to use')
    pending = Integer(description='Counter for pending deliveries needed')
    pickup = DateTime(description='When was this picked up by the node')
    status = String(description='Status of the delivery')
    study_id = Integer(description='FK. The study to push')
    study = Study(description='The study to push')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class StudyPushStatus(BaseModel):
    """StudyPushStatus."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    destination_id = Integer(description='FK. The destination')
    destination = Destination(description='The destination')
    phi_namespace = Integer(description='FK. PHI namespace to allow for scoping the filter down')
    phi_namespace_obj = Namespace(description='PHI namespace to allow for scoping the filter down')
    status = String(description='Current status - pe&#39;N&#39;ding, &#39;I&#39;n-process, &#39;P&#39;artial, &#39;S&#39;uccess, &#39;F&#39;ailure')
    study_id = Integer(description='FK. The study')
    study = Study(description='The study')
    study_push_id = Integer(description='FK. The latest push')
    study_push = StudyPush(description='The latest push')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class StudyQuestion(BaseModel):
    """StudyQuestion."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    account_id = Integer(description='FK. The study and account id')
    account = Account(description='The study and account id')
    answer = String(description='Question and answer')
    answered = DateTime(description='When was this picked up and answered by the ai stack')
    detail = String(description='Question and answer')
    next_question = Integer(description='Id of the next question to ask when this one is answered')
    pickup = DateTime(description='When was this picked up and answered by the ai stack')
    question = String(description='Question and answer')
    raw_answer = String(description='Question and answer')
    study_id = Integer(description='FK. The study and account id')
    study = Study(description='The study and account id')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class StudyShare(BaseModel):
    """StudyShare."""
    
    id = Integer(description='Primary key for internal use')
    account_id = Integer(description='FK. Who it is shared with')
    account = Account(description='Who it is shared with')
    group_id = Integer(description='FK. Who it is shared with')
    group = Group(description='Who it is shared with')
    location_id = Integer(description='FK. Who it is shared with')
    location = Location(description='Who it is shared with')
    message = String(description='Share message')
    new_study_id = Integer(description='FK. Id of the new study created by the share')
    new_study = Study(description='Id of the new study created by the share')
    study_id = Integer(description='FK. Primary key for internal use')
    study = Study(description='Primary key for internal use')
    user_id = Integer(description='FK. Who it is shared with')
    user = User(description='Who it is shared with')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class StudyShareAi(BaseModel):
    """StudyShareAi."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    account_id = Integer(description='FK. UUID for external use')
    account = Account(description='UUID for external use')
    from_account_id = Integer(description='FK. Id and account of the study it was shared from')
    from_account = Account(description='Id and account of the study it was shared from')
    from_study_id = Integer(description='FK. Id and account of the study it was shared from')
    from_study = Study(description='Id and account of the study it was shared from')
    study_id = Integer(description='FK. UUID for external use')
    study = Study(description='UUID for external use')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class StudyShareRsna(BaseModel):
    """StudyShareRsna."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    exam_id = String(description='The PIN and Exam id')
    pin = String(description='The PIN and Exam id')
    reason = String(description='Reason the delivery failed')
    status = String(description='Status of the delivery')
    study_id = Integer(description='FK. The study shared')
    study = Study(description='The study shared')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class StudyStar(BaseModel):
    """StudyStar."""
    
    id = Integer(description='Primary key for internal use')
    star = Boolean(description='The study star')
    study_id = Integer(description='FK. ')
    study = Study(description='')
    user_id = Integer(description='FK. ')
    user = User(description='')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class StudyStatusLock(BaseModel):
    """StudyStatusLock."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    study_id = Integer(description='FK. The study and user id')
    study = Study(description='The study and user id')
    user_id = Integer(description='FK. The study and user id')
    user = User(description='The study and user id')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class StudyTiming(BaseModel):
    """StudyTiming."""
    
    id = Integer(description='Primary key for internal use')
    event = String(description='The event')
    node_id = Integer(description='FK. Node id')
    node = Node(description='Node id')
    size = Integer(description='The event')
    storage_namespace = Integer(description='FK. The study uid and storage namespace')
    storage_namespace_obj = Namespace(description='The study uid and storage namespace')
    study_uid = String(description='The study uid and storage namespace')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')


class System(BaseModel):
    """System."""
    
    id = Integer(description='Primary key for internal use')
    ai_password = String(description='AI stack basic auth credentials')
    ai_username = String(description='AI stack basic auth credentials')
    archive = Dict(description='The archive settings')
    athena_pk = String(description='Athena key and secret')
    athena_sk = String(description='Athena key and secret')
    aws_pk = String(description='AWS information')
    aws_region = String(description='AWS information')
    aws_sk = String(description='AWS information')
    cache = Boolean(description='Cache new studies images')
    captcha_pk = String(description='Captcha public key')
    captcha_sk = String(description='Captcha secret key')
    database_version = Integer(description='Database version')
    drchrono_client_id = String(description='Drchrono information')
    drchrono_client_secret = String(description='Drchrono information')
    drchrono_redirect_uri = String(description='Drchrono information')
    email_from = String(description='From email address and name')
    email_from_name = String(description='From email address and name')
    email_validation = Boolean(description='Flag to enable email validation')
    enhanced_security = Boolean(description='Enable enhanced security')
    global_purge = Boolean(description='Flag to enable global purge rule support')
    google_client_id = String(description='Google information')
    google_client_secret = String(description='Google information')
    google_service_account = String(description='Google information')
    hide_help_tool = Boolean(description='Flag to hide the help tool globally')
    indicator_html = String(description='HTML for the terms of use, privacy policy and indicators of use')
    indicator_md5 = String(description='MD5 sums of the terms of use, privacy policy and indicators of use')
    log_days = Integer(description='Number of days to retain logs for')
    passwdqc = String(description='Password controls')
    passwdqc_description = String(description='Password controls')
    phr_permissions = String(description='The PHR  permissions over-ride')
    privacy_html = String(description='HTML for the terms of use, privacy policy and indicators of use')
    privacy_md5 = String(description='MD5 sums of the terms of use, privacy policy and indicators of use')
    rsna_xds = String(description='RSNA XDS server')
    stripe_ca = String(description='Stripe connect client id')
    stripe_pk = String(description='Stripe public key')
    stripe_sk = String(description='Stripe secret key')
    stripe_uri = String(description='Stripe URI')
    terms_html = String(description='HTML for the terms of use, privacy policy and indicators of use')
    terms_md5 = String(description='MD5 sums of the terms of use, privacy policy and indicators of use')
    twilio_from = String(description='Twilio key, secret and from phone number')
    twilio_pk = String(description='Twilio key, secret and from phone number')
    twilio_sk = String(description='Twilio key, secret and from phone number')
    user_settings = Dict(description='Default user settings')
    watchdog_host = String(description='Watch dog host, used if not set in site.conf')
    websocket_domain = String(description='Websocket domain')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class Tag(BaseModel):
    """Tag."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    object = String(description='The associated user and object class')
    tag = String(description='The tag')
    user_id = Integer(description='FK. The associated user and object class')
    user = User(description='The associated user and object class')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class TagObject(BaseModel):
    """TagObject."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    object = String(description='The user and object fields')
    object_id = Integer(description='FK. The user and object fields')
    tags = Dict(description='The tags')
    user_id = Integer(description='FK. The user and object fields')
    user = User(description='The user and object fields')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class TemplateAssign(BaseModel):
    """TemplateAssign."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    account_id = Integer(description='FK. Account the template is for')
    account = Account(description='Account the template is for')
    name = String(description='Template name, this is the directory name for the template')
    version = String(description='Version, this is the file name to serve')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class Terminology(BaseModel):
    """Terminology."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    account_id = Integer(description='FK. Account id if we have an over ride')
    account = Account(description='Account id if we have an over ride')
    language = String(description='ISO 639-1 code of the language')
    tag = String(description='Dynamic tag')
    value = String(description='The translated value')
    vanity = String(description='Vanity override')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class TrainingAccount(BaseModel):
    """TrainingAccount."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    account_id = Integer(description='FK. ')
    account = Account(description='')
    form_description = String(description='')
    form_number = String(description='')
    group_description = String(description='')
    group_number = Integer(description='')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class TrainingUser(BaseModel):
    """TrainingUser."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    form_number = String(description='')
    results = Dict(description='The form data from the training')
    user_id = Integer(description='FK. ')
    user = User(description='')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class User(BaseModel):
    """User."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    access_token = String(description='Stripe access token')
    billing = Boolean(description='Are they a billing person')
    blocked = Boolean(description='Is a the user blocked from the system')
    disabled = Boolean(description='Is a the user disabled from the system')
    email = String(description='Email address')
    email_validation = Boolean(description='2 - email is validated')
    event_approve = Boolean(description='The event flags for the personal namespace')
    event_harvest = Boolean(description='The event flags for the personal namespace')
    event_link = Boolean(description='The event flags for the personal namespace')
    event_link_mine = Boolean(description='The event flags for the personal namespace')
    event_message = Boolean(description='The event flags for the personal namespace')
    event_new_report = Boolean(description='The event flags for the personal namespace')
    event_share = Boolean(description='The event flags for the personal namespace')
    event_status_change = Boolean(description='The event flags for the personal namespace')
    event_study_comment = Boolean(description='The event flags for the personal namespace')
    event_thin_study_fail = Boolean(description='The event flags for the personal namespace')
    event_thin_study_success = Boolean(description='The event flags for the personal namespace')
    event_upload = Boolean(description='The event flags for the personal namespace')
    event_upload_fail = Boolean(description='The event flags for the personal namespace')
    first = String(description='Name')
    indicator_md5 = String(description='MD5 sums of the accepted terms of use, privacy policy and indicators of use')
    last = String(description='Name')
    last_login = DateTime(description='The last login time')
    mobile_phone = String(description='Mobile phone')
    namespace_id = Integer(description='FK. Their namespace')
    namespace = Namespace(description='Their namespace')
    npi = String(description='NPI number')
    oauth = String(description='OAuth id and refresh token')
    password = String(description='Password')
    pin_required = Boolean(description='Is a PIN required for login')
    privacy_md5 = String(description='MD5 sums of the accepted terms of use, privacy policy and indicators of use')
    refresh_token = String(description='OAuth id and refresh token')
    signature = String(description='Signature image (base64)')
    support = Boolean(description='Are they a support person')
    sysadmin = Boolean(description='Are they a system administrator')
    terms_md5 = String(description='MD5 sums of the accepted terms of use, privacy policy and indicators of use')
    time_zone = String(description='Timezone')
    token = String(description='Shared secret for TOKEN authentication')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class UserAccount(BaseModel):
    """UserAccount."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    account_alias = String(description='The users alias for the account')
    account_email = String(description='The email for account. One needed if this is different that the users email')
    account_id = Integer(description='FK. Mapping between the user and account')
    account = Account(description='Mapping between the user and account')
    account_login = String(description='The users login name for the account')
    account_password = String(description='The users password in the account')
    customfields = Dict(description='Custom fields')
    event_approve = Boolean(description='The event flags')
    event_harvest = Boolean(description='The event flags')
    event_join = Boolean(description='The event flags')
    event_link = Boolean(description='The event flags')
    event_link_mine = Boolean(description='The event flags')
    event_message = Boolean(description='The event flags')
    event_new_report = Boolean(description='The event flags')
    event_node = Boolean(description='The event flags')
    event_purge = Boolean(description='The event flags')
    event_share = Boolean(description='The event flags')
    event_status_change = Boolean(description='The event flags')
    event_study_comment = Boolean(description='The event flags')
    event_thin_study_fail = Boolean(description='The event flags')
    event_thin_study_success = Boolean(description='The event flags')
    event_upload = Boolean(description='The event flags')
    event_upload_fail = Boolean(description='The event flags')
    global = Boolean(description='This user is automatically added to every group and location in the account')
    last_reset = DateTime(description='Time the password was last reset')
    max_sessions = Integer(description='Override for the max number of sessions a user can have')
    password_reset = Boolean(description='Flag to reset the password')
    role_id = Integer(description='FK. Role')
    role = Role(description='Role')
    session_expire = Integer(description='Minutes before an idle session expires, this is an override of the account setting')
    settings = Dict(description='Account settings overrides')
    user_id = Integer(description='FK. Mapping between the user and account')
    user = User(description='Mapping between the user and account')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class UserAws(BaseModel):
    """UserAws."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    customer_identifier = String(description='The AWS customer identifier')
    product_code = String(description='The product they are registered for')
    subscription_state = String(description='The state of the subscription')
    user_id = Integer(description='FK. User id')
    user = User(description='User id')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class UserGroup(BaseModel):
    """UserGroup."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    event_approve = Boolean(description='The event flags')
    event_harvest = Boolean(description='The event flags')
    event_link = Boolean(description='The event flags')
    event_link_mine = Boolean(description='The event flags')
    event_message = Boolean(description='The event flags')
    event_new_report = Boolean(description='The event flags')
    event_node = Boolean(description='The event flags')
    event_share = Boolean(description='The event flags')
    event_status_change = Boolean(description='The event flags')
    event_study_comment = Boolean(description='The event flags')
    event_thin_study_fail = Boolean(description='The event flags')
    event_thin_study_success = Boolean(description='The event flags')
    event_upload = Boolean(description='The event flags')
    event_upload_fail = Boolean(description='The event flags')
    group_id = Integer(description='FK. Mapping between the user and group')
    group = Group(description='Mapping between the user and group')
    no_physician_alias_share = Boolean(description='Do not do a physician alias share into this group')
    role_id = Integer(description='FK. Role over ride for the user in this group')
    role = Role(description='Role over ride for the user in this group')
    user_id = Integer(description='FK. Mapping between the user and group')
    user = User(description='Mapping between the user and group')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class UserInvite(BaseModel):
    """UserInvite."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    account_id = Integer(description='FK. Account the invitation is for')
    account = Account(description='Account the invitation is for')
    email = String(description='Email address to invite')
    groups = String(description='JSON hashes of the groups and locations to add them to with the role as the key value')
    locations = String(description='JSON hashes of the groups and locations to add them to with the role as the key value')
    role_id = Integer(description='FK. Role the invitation is for')
    role = Role(description='Role the invitation is for')
    user_id = Integer(description='FK. Id of the user who accepted the invitation')
    user = User(description='Id of the user who accepted the invitation')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class UserInviteShare(BaseModel):
    """UserInviteShare."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    email = String(description='Email address to invite')
    message = String(description='Share message')
    study_id = Integer(description='FK. Id for the study to be shared')
    study = Study(description='Id for the study to be shared')
    user_id = Integer(description='FK. Id the invitation is from')
    user = User(description='Id the invitation is from')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class UserLocation(BaseModel):
    """UserLocation."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    event_approve = Boolean(description='The event flags')
    event_harvest = Boolean(description='The event flags')
    event_link = Boolean(description='The event flags')
    event_link_mine = Boolean(description='The event flags')
    event_message = Boolean(description='The event flags')
    event_new_report = Boolean(description='The event flags')
    event_node = Boolean(description='The event flags')
    event_share = Boolean(description='The event flags')
    event_status_change = Boolean(description='The event flags')
    event_study_comment = Boolean(description='The event flags')
    event_thin_study_fail = Boolean(description='The event flags')
    event_thin_study_success = Boolean(description='The event flags')
    event_upload = Boolean(description='The event flags')
    event_upload_fail = Boolean(description='The event flags')
    location_id = Integer(description='FK. Mapping between the user and location')
    location = Location(description='Mapping between the user and location')
    no_physician_alias_share = Boolean(description='Do not do a physician alias share into this location')
    role_id = Integer(description='FK. Role over ride for the user in this location')
    role = Role(description='Role over ride for the user in this location')
    user_id = Integer(description='FK. Mapping between the user and location')
    user = User(description='Mapping between the user and location')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class Validate(BaseModel):
    """Validate."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    account_id = Integer(description='FK. The associated account')
    account = Account(description='The associated account')
    conditions = String(description='The validate conditions')
    name = String(description='Name')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class Webhook(BaseModel):
    """Webhook."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    account_id = Integer(description='FK. The account')
    account = Account(description='The account')
    auth = String(description='The webhook auth')
    by_accession_number = Boolean(description='Expand the once to check by accession_number as well')
    by_uid = Boolean(description='Expand the once to check by study_uid as well')
    cron = String(description='Cron string for a cron type of webhook')
    delay = Integer(description='Number of seconds to delay running this webhook after it is triggered')
    event = String(description='The event to trigger the webhook for')
    filter_field = String(description='Filter field and regexp')
    filter_regexp = String(description='Filter field and regexp')
    last_error = String(description='The last error the webhook had')
    max_age = Integer(description='Ignore studies that are more than this number of days old')
    method = String(description='Call method (POST,GET,POST_JSON,PUT)')
    name = String(description='Name')
    node_id = Integer(description='FK. The node id to proxy the call through')
    node = Node(description='The node id to proxy the call through')
    once = Boolean(description='Run this only once for a specific study')
    parameters = String(description='The parameters for the call')
    retry = Boolean(description='Retry if it fails and a counter to track the retries')
    retry_count = Integer(description='Retry if it fails and a counter to track the retries')
    sid_user_id = Integer(description='FK. The user id to generate a sid as')
    sid_user = User(description='The user id to generate a sid as')
    suspended = Boolean(description='Suspend this hook from running')
    url = String(description='The URL to call')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class WebhookNode(BaseModel):
    """WebhookNode."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    method = String(description='Call method')
    node_id = Integer(description='FK. The node id to proxy the call through')
    node = Node(description='The node id to proxy the call through')
    parameters = String(description='The parameters for the call')
    pickup = DateTime(description='When was this picked up by the node')
    status = String(description='Status of the delivery')
    url = String(description='The URL to call')
    webhook_id = Integer(description='FK. The webhook id')
    webhook = Webhook(description='The webhook id')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')


class WebhookOnce(BaseModel):
    """WebhookOnce."""
    
    id = Integer(description='Primary key for internal use')
    uuid = String(description='UUID for external use')
    study_id = Integer(description='FK. The webhook and study id')
    study = Study(description='The webhook and study id')
    webhook_id = Integer(description='FK. The webhook and study id')
    webhook = Webhook(description='The webhook and study id')
    created = DateTime(description='Timestamp when the record was created')
    created_by = Integer(description='FK. ID of the user who created the record')
    created_by_obj = User(description='ID of the user who created the record')
    updated = DateTime(description='Timestamp when the record was last updated')
    updated_by = Integer(description='FK. ID of the user who updated the record')
    updated_by_obj = User(description='ID of the user who updated the record')
