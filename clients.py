from connection import APIConn


class WHMCSClient:

    # cast groups
    intgroup = ['id', 'groupid']
    boolgroup = ['taxexempt',
               'latefeeoveride',
               'overideduenotices',
               'separateinvoices',
               'disableautocc',
               'skipvalidation',
               'noemail']
    reqgroup = ['firstname',
                'lastname',
                'email',
                'address1',
                'city',
                'state',
                'postcode',
                'phonenumber']
    # Integers
    id = 0
    groupid = '' # used to assign the client to a client group

    # String
    firstname = '' # required
    lastname = '' # required
    email = '' # required
    address1 = '' # required
    address2 = ''
    city = '' # required
    state = '' # required
    postcode = '' # required
    country = '' # two letter ISO country code
    phonenumber = '' # required
    password2 = '' # password for the new user account
    currency = '' # the ID of the currency to set the user to
    notes = ''
    cctype = '' # Visa, Mastercard, etc...
    cardnum = ''
    expdate = '' # in the format MMYY
    startdate = ''
    issuenumber = ''
    customfields = '' # a base64 encoded serialized array of custom field values
        
    companyname = ''
    address2 = ''
    datecreated = None
    status = ''

    securityqid = ''
    securityqans = ''
    credit = ''

    # Boolean
    taxexempt = False
    latefeeoveride = False
    overideduenotices = False
    separateinvoices = False
    disableautocc = False
    skipvalidation = False # set true to not validate or check required fields
    noemail = False # pass as true to surpress the client signup welcome email sending


    language = ''
    lastlogin = ''
    billingcid = ''
    domainemails = ''
    generalemails = ''
    invoiceemails = ''
    productemails = ''
    supportemails = ''
    countryname = ''
    customfields = {}

    def __init__(self, data=None, *args, **kwargs):
        # assume data is a a dictionary of information
        if data is not None:
            for key, value in data.iteritems():
                if key.find('customfield') != -1:
                    self.customfields[key] = value
                else:
                    if key in self.boolgroup:
                        if value.strip() == 'on':
                            setattr(self, key, True)
                    elif key in self.intgroup:
                        setattr(self, key, int(value.strip()))
                    else:
                        setattr(self, key, value.strip())

    def save(self):
        data = self.clean()
        conn = APIConn()
        
        if self.id == 0:
            data['action'] = 'addclient'
        else:
            data['action'] = 'updateclient'
            data['clientid'] = self.id

        resp = conn.request(data)

        self.id = int(resp['clientid'])

    def delete(self);
        if self.id == 0:
            return False
        conn = APIConn()
        data = {}
        data = {'action': 'deleteclient', 'clientid': self.id}
        resp = conn.request(data)
        return True

    def close(self):
        if self.id == 0:
            return False
        conn = APIConn()
        data = {'action': 'closeclient', 'clientid': self.id}
        resp = con.request(data)
        return True

    def clean(self):
        # make sure all required fields are there and strip whitespace
        cleaned_data = {}
        for key in self.reqgroup:
            if key not in self.__dict__:
                raise ValidationError('%s is required' % key)
        for key, value in self.__dict__.iteritems():
            if key in self.reqgroup and value == '':
                raise ValidationError('%s cannot be blank' % key)
            try:
                cleaned_data[key] = value.strip()
            except AttributeError:
                cleaned_data[key] = value

        return cleaned_data

class ValidationError(Exception):
    def __init__(self, value):
        self.parameter = value
    def __str__(self):
        return repr(self.parameter)
