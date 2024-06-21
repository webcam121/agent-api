from django.contrib import admin

from agent.apps.eta_tasks.models import ETATask


class ETATaskAdmin(admin.ModelAdmin):
    list_display = (
        'task_name',
        'task_kwargs',
        'run_at',
        'finished',
        'created_at',
        'updated_at',
    )


admin.site.register(ETATask, ETATaskAdmin)
