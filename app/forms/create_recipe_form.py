from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SelectField, FieldList, FormField
from wtforms.validators import InputRequired, Optional, Length, ValidationError

POPULAR_CUISINES = [
    ('American', 'American'),
    ('Argentinian', 'Argentinian'),
    ('Brazilian', 'Brazilian'),
    ('British', 'British'),
    ('Caribbean', 'Caribbean'),
    ('Chinese', 'Chinese'),
    ('Colombian', 'Colombian'),
    ('Ethiopian', 'Ethiopian'),
    ('Filipino', 'Filipino'),
    ('French', 'French'),
    ('Fusion', 'Fusion'),
    ('German', 'German'),
    ('Greek', 'Greek'),
    ('Indian', 'Indian'),
    ('Italian', 'Italian'),
    ('Japanese', 'Japanese'),
    ('Korean', 'Korean'),
    ('Mediterranean', 'Mediterranean'),
    ('Mexican', 'Mexican'),
    ('Middle Eastern', 'Middle Eastern'),
    ('Moroccan', 'Moroccan'),
    ('Nigerian', 'Nigerian'),
    ('Peruvian', 'Peruvian'),
    ('South African', 'South African'),
    ('Spanish', 'Spanish'),
    ('Thai', 'Thai'),
    ('Vietnamese', 'Vietnamese'),
    ('Other', 'Other'),
]



# Ingredient and Instruction Form to encapsulate individual fields
class IngredientForm(FlaskForm):
    ingredient = StringField('Ingredient')
    class Meta:
        csrf = False

class InstructionForm(FlaskForm):
    instruction = StringField('Instruction')
    class Meta:
        csrf = False


class CreateRecipeForm(FlaskForm):
    # Basic recipe information
    name = StringField('name', validators=[Length(max=100)])
    yield_servings = IntegerField("servings")
    prep_time = IntegerField("prep time")
    cook_time = IntegerField("cook time")
    total_time = IntegerField("total time")

    # Select cuisine from list defined above
    cuisine = SelectField('cuisine', choices=POPULAR_CUISINES)
    short_description = StringField("create a tagline for your recipe")

    # Description field
    description = TextAreaField('share a favorite memory, story, or who this recipe reminds you about', validators=[Length(max=500)])

    # Dynamic Ingredients and Instructions
    ingredients = FieldList(FormField(IngredientForm), min_entries=1)
    instructions = FieldList(FormField(InstructionForm), min_entries=1)

    # Tags field: users input a comma-separated string
    tags = StringField('enter tags separated by commas')
