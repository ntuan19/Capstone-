from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, FileField, DecimalField, SelectField, HiddenField, SelectMultipleField
from wtforms.validators import DataRequired, Length, ValidationError


class InvestmentForm(FlaskForm):
    business_registration = StringField('Business Registration', validators=[DataRequired(), Length(max=50)])
    business_address = StringField('Business Address', validators=[DataRequired(), Length(max=100)])
    company_name = StringField("Company's Name", validators=[DataRequired(), Length(max=50)])
    current_rounds = IntegerField('Current Rounds of Investments', validators=[DataRequired()])
    total_funding_wanted = DecimalField('Total Funding Wanted', validators=[DataRequired()])
    currency = SelectField("Currency", choices=[('USD', 'USD'), ('EUR', 'EUR'), ('GBP', 'GBP'), ('JPY', 'JPY')])
    pictures = FileField('Pictures')
    financial_situation = TextAreaField('Financial Situation', validators=[DataRequired()])
    approved = HiddenField('Approved', default='pending')
    business_topics = SelectMultipleField("Currency", choices=[('Real Estate', '#RealEstate'), ('Pharmacy', '#Pharmacy'), ('Fintech', '#Fintech'), ('Healthcare', '#Healthcare'), ('Technology', '#Technology'), ('Space', '#Space'), ('Agriculture', '#Agriculture'), ('Education', '#Education'), ('Energy', '#Energy'), ('Transportation', '#Transportation'), ('Manufacturing', '#Manufacturing'), ('Retail', '#Retail'), ('Hospitality', '#Hospitality'), ('Construction', '#Construction')])
    link_documents = StringField("Document Links",validators=[DataRequired()])

    def validate_business(form, field):
        if len(field.data) > 3:
            raise ValidationError('You can select a maximum of 3 options.')


# class InvestmentForm(FlaskForm):
#     business_registration = StringField('Business Registration', validators=[DataRequired(), Length(max=50)])
#     business_address = StringField('Business Address', validators=[DataRequired(), Length(max=100)])
#     company_name = StringField("Company's Name", validators=[DataRequired(), Length(max=50)])
#     current_rounds = IntegerField('Current Rounds of Investments', validators=[DataRequired()])
#     total_funding_wanted = DecimalField('Total Funding Wanted', validators=[DataRequired()])
#     currency = SelectField("Currency", choices=[('USD', 'USD'), ('EUR', 'EUR'), ('GBP', 'GBP'), ('JPY', 'JPY')])
#     presentation = FileField('Presentation')
#     pictures = FileField('Pictures')
#     financial_situation = TextAreaField('Financial Situation', validators=[DataRequired()])
#     approved = HiddenField('Approved', default='pending')
#     tax_returns = FileField("Tax Returns",validators=[DataRequired()])
#     financial_statements = FileField("Financial Statements",validators=[DataRequired()])
#     customers_dataset = FileField("Customer Base",validators=[DataRequired()])
#     supporting_documents = FileField("Supporting Documents")

