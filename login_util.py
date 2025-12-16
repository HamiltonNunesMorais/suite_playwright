import settings

async def login(page):
    await page.click("text=Log in")
    await page.fill("input#Email", settings.EMAIL)
    await page.fill("input#Password", settings.PASSWORD)
    await page.click("input[value='Log in']")
