class BasePage:
    def __init__(self, page):
        self.page = page

    async def go_to(self, url: str):
        await self.page.goto(url)

    async def get_text(self, selector: str):
        return await self.page.text_content(selector)

    async def click(self, selector: str):
        await self.page.click(selector)

    async def fill(self, selector: str, value: str):
        await self.page.fill(selector, value)

    async def wait_for_selector(self, selector: str):
        await self.page.wait_for_selector(selector)
