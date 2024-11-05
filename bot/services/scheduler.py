from datetime import datetime, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

scheduler = AsyncIOScheduler()
tasks = {}

async def send_reminder(user_id: int, plant_name: str, context):
  """Отправляет пользователю напоминание о поливе растения."""
  await context.bot.send_message(chat_id=user_id, text=f"<b>Напоминание: Полейте {plant_name}!</b>")


def schedule_reminders(user_id: int, plant_name: str, frequency: int, context):
  """Создает и запускает задачу напоминания о поливе растения."""
  job_id = f"{user_id}_{plant_name}"
  if job_id in tasks:
    cancel_reminders(user_id, plant_name)

  job = scheduler.add_job(
    send_reminder,
    "interval",
    days=frequency,
    args=[user_id, plant_name, context],
    id=job_id,
    next_run_time=datetime.now() + timedelta(days=frequency)
  )
  tasks[job_id] = job


def cancel_reminders(user_id: int, plant_name: str):
  """Отменяет задачу напоминания о поливе растения."""
  job_id = f"{user_id}_{plant_name}"
  if job_id in tasks:
    scheduler.remove_job(job_id)
    del tasks[job_id]


async def toggle_notifications(user_id: int, plant_name: str, frequency_days: int, enable: bool, context):
  """Включает или отключает уведомления о поливе растения."""
  if enable:
    schedule_reminders(user_id, plant_name, frequency_days, context)
  else:
    cancel_reminders(user_id, plant_name)