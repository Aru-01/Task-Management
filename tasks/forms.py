from django import forms
from tasks.models import Task, TaskDetail


# django form
class TaskForm(forms.Form):
    title = forms.CharField(max_length=250, label="Task Title")
    description = forms.CharField(widget=forms.Textarea, label="Task Description")
    due_date = forms.DateField(widget=forms.SelectDateWidget, label="Due Date")
    assigned_to = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, choices=[], label="Assigned To"
    )

    def __init__(self, *args, **kwargs):
        employees = kwargs.pop("employees", [])
        super().__init__(*args, **kwargs)
        self.fields["assigned_to"].choices = [(emp.id, emp.name) for emp in employees]


class StyledFormMixin:
    """mixin to apply style to form field"""

    default_classes = "px-4 py-2 border border-gray-300 rounded-lg shadow-sm text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-200 ease-in-out bg-gradient-to-r from-white to-gray-50 hover:shadow-lg"

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update(
                    {
                        "class": f"{self.default_classes} w-full pl-2",
                        "placeholder": f"Enter {field.label.lower()}...",
                    }
                )
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update(
                    {
                        "class": f"{self.default_classes} w-full",
                        "placeholder": f"Enter {field.label.lower()}...",
                        "rows": 5,
                    }
                )
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update(
                    {
                        "class": f"{self.default_classes}",
                    }
                )
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update(
                    {
                        "class": f"space-y-2 p-4 bg-white border border-gray-200 rounded- shadow-sm",
                    }
                )
            else:
                pass


# django model form
class TaskModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "due_date", "assigned_to"]
        widgets = {
            "due_date": forms.SelectDateWidget(
                # attrs={
                #     "class": "px-4 py-2 border border-gray-300 rounded-md shadow-sm          text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500          focus:border-blue-500 transition duration-200 ease-in-out          bg-gradient-to-r from-white to-gray-50 hover:shadow-md"
                # }
            ),
            "assigned_to": forms.CheckboxSelectMultiple(
                # attrs={
                #     "class": "space-y-2 p-4 bg-white border border-gray-200 rounded-md shadow-sm"
                # }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()


class TaskDetailModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = TaskDetail
        fields = ["priority", "notes"]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()