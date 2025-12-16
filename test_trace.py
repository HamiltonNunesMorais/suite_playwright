import os
import time
import pytest
from playwright.async_api import async_playwright, expect
import settings
from login_util import login

@pytest.mark.asyncio
async def test_e2e_checkout_terms_trace():
    # Garante que as pastas existem
    os.makedirs("videos", exist_ok=True)
    os.makedirs("screenshots", exist_ok=True)
    os.makedirs("traces", exist_ok=True)

    timestamp = time.strftime("%Y%m%d-%H%M%S")
    trace_path = f"traces/checkout_terms_{timestamp}.zip"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=300)
        context = await browser.new_context(
            record_video_dir="videos/",
            record_video_size={"width": 1280, "height": 720}
        )

        # Inicia o trace com nível detalhado
        await context.tracing.start(screenshots=True, snapshots=True, sources=True)

        page = await context.new_page()

        # 1. Login
        await page.goto(settings.BASE_URL)
        await login(page)
        await expect(page.get_by_text("Log out")).to_be_visible()

        # 2. Navegar até Computers → Desktops → Produto
        await page.get_by_role("link", name="Computers").first.click()
        await page.get_by_role("link", name="Desktops").first.click()
        await page.get_by_role("link", name="Picture of Build your own cheap computer").click()

        # 3. Scroll até o botão Add to cart e clicar
        add_btn = page.locator("#add-to-cart-button-72")
        await add_btn.scroll_into_view_if_needed()
        await expect(add_btn).to_be_visible()
        await add_btn.click()

        # 4. Validar mensagem de confirmação + screenshot
        await expect(page.get_by_text("The product has been added to")).to_be_visible()
        await page.screenshot(path=f"screenshots/confirmation_{timestamp}.png")

        # 5. Ir ao carrinho
        await page.goto("https://demowebshop.tricentis.com/cart")
        await expect(
            page.locator("table.cart").get_by_role("link", name="Build your own cheap computer")
        ).to_be_visible()

        # 6. Checkout sem aceitar termos → abre modal
        checkout_btn = page.get_by_role("button", name="Checkout")
        await checkout_btn.click()
        await expect(page.get_by_role("button", name="close")).to_be_visible()
        await page.get_by_role("button", name="close").click()

        # 7. Marcar termos e prosseguir
        terms = page.locator("#termsofservice")
        await terms.check()
        await checkout_btn.click()

        # 8. Validar que caiu na página de Billing address
        await expect(page.get_by_text("Billing address")).to_be_visible()

        # Para e salva o trace
        await context.tracing.stop(path=trace_path)

        await context.close()
        await browser.close()
