import asyncio
import time
import customtkinter
from playwright.async_api import async_playwright
from datetime import datetime


class LoginWindow:

    def __init__(self):
            self.email = None
            self.password = None
            
            customtkinter.set_appearance_mode("System")
            customtkinter.set_default_color_theme("green")

            root = customtkinter.CTk()
            root.geometry("500x350")

            def login():
                self.email = entry1.get()
                root.destroy()

            def close_window():
                root.destroy()

            frame = customtkinter.CTkFrame(master=root)
            frame.pack(pady=20, padx=60, fill="both", expand=True)

            label = customtkinter.CTkLabel(master=frame, text="Login System")
            label.pack(pady=12, padx=10)

            entry1 = customtkinter.CTkEntry(master=frame, placeholder_text="Username")
            entry1.pack(pady=12, padx=10)

       
            button = customtkinter.CTkButton(master=frame, text="Login", command=login)
            button.pack(pady=12, padx=10)
            root.bind('<Return>', lambda event: login())

            
            root.bind('<Return>', lambda event: login())
            root.protocol("WM_DELETE_WINDOW", close_window)

            root.mainloop()

async def download_excel(page):
    choices_selector = 'a[title="Volby"]'
    excel_export_selector = 'a[title="Exportovat do Excelu"]'

    await page.click(choices_selector)
    await page.click(excel_export_selector)


async def choose_course(page):
    button_selector3 = "input[name='course_id']"
    await page.click(button_selector3)

    first_id = page.locator('li:has-text("-- AKTIVNÍ KURZY ---")')
    last_id = page.locator('li:has-text("-- SUPLOVANÉ A NEZAPSANÉ KURZY --")')

    start = int("".join(filter(str.isdigit, await first_id.get_attribute("id"))))
    end = int("".join(filter(str.isdigit, await last_id.get_attribute("id"))))

    for i in range(start + 1, end + 1):
        id = "cbr_" + str(i)
        print(id)
        button_selector3 = "input[name='course_id']"
        await page.click(button_selector3)

        await page.wait_for_load_state("networkidle")

        course = page.locator(f'li[id="{id}"]')
        await course.click()
        id2 = "cbr_" + str(i - 1)
        if id2 != "cbr_1":
            name = await page.locator(f'li[id="{id2}"]').inner_text()

            await download_excel(page)
            async with page.expect_download() as download_info:
                today = datetime.today().strftime('%d-%m-%Y')

                download = await download_info.value
                await download.save_as(f".\{email} {today}\{name}.xlsx")
        else:
            continue


async def login():
    global email
    async with async_playwright() as playwright:
        root = customtkinter.CTk()
        root.geometry("500x350")
        frame = customtkinter.CTkFrame(master=root)
        frame.pack(pady=20, padx=60, fill="both", expand=True)

        entry2 = customtkinter.CTkEntry(master=frame, placeholder_text="Password", show="*")
        entry2.pack(pady=12, padx=10)
        
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        while True:
                try:
                    await page.goto("https://uuidentity.plus4u.net/uu-identitymanagement-maing01/a9b105aff2744771be4daa8361954677/login?acrValues=low%20standard%20high%20veryHigh&clientId=07391806753a42cd8110140eb30683b9&uiLocales=cs&state=6jkPmRIkKca7teCO.g7RbWxfrgnrd7zkdlcEWqhNHlynG2db-zqZ2rcZPUQxsjoQxJHH4ktvOlg4-9EyfAmbUSla11voHKy3yBeaK-MoQ9cINLepbHmrdszPP-2kdbUQj8Hm_HKIM7KEhxZY25-jjuxh_zqALt2hkqD0EmYCDG-Oz4NP7dK-qDmrCyPnS3p5RSxImewr-KA4sYMpyMKo6L2wMF-ZUT-pEzMdDUOUs8hcOgzO5VCaEJxozpIFN2FIj_e5WsS_dLo2cmhvmXn1-DmjO4nSIr2q_DQYd2FGYy8uofvOh0llFjtZTg-BXswbhvIfTxrtKVnA1PKwVwfQHcHahisLC7zYgLm_DW5VJ3AE1HVzQ6YfiZmaMk9Ma9TPNA_7njXGrSOFp28zHBCZejycA3VTFzOUWUxAot3RtM0MJGYyshve63Fwg42oiSafcdkQOqEl3cdZMfHdaA8JHk3KZW2v1s5EfvbAzCR9t_XbfL7eOpLEnhrOuz3N33GodOhOagiFBKh46afREKQkG-JQ4VIGfjL90YAQN7iKI0Ai5ER6F8NYX1TieaAzS5Z55ANWzmaD8tSorB7wHYL8PaT2gCwfC2rdinliiMg1QHAfhVIz7SiPEvDN0")
                
                    await page.wait_for_load_state("networkidle")
                    button = await page.query_selector('button:has-text("Microsoft")')
                    await button.click()
                  
                    await page.wait_for_load_state("networkidle")

                    login_window = LoginWindow()
                    email = login_window.email
                    print(email)
                    await page.wait_for_load_state("networkidle")
                    email_selector = "input[type='email']"
                    await page.fill(email_selector, f"{email}")

                    await page.wait_for_load_state("networkidle")

                    sign_in_button_selector = "input[type='submit']"
                    await page.click(sign_in_button_selector)

                    await page.wait_for_load_state("networkidle")
                    password_selector = "input[type='password']"
                    await page.fill(password_selector, entry2.get())
                    await page.click(sign_in_button_selector)
                    await page.wait_for_load_state("networkidle")

        
                    await page.wait_for_load_state("networkidle")
                    print("checking password")
                    dontKeepSignIn = "input[id='idBtn_Back']"
                    await page.click(dontKeepSignIn)
                    evaluation_selector = "#lid221"
                    await page.click(evaluation_selector)
                    break

                except:
                    print("wrong credentials")
        
        await choose_course(page)
        await context.close()
        await browser.close()

async def main():
    start_time = time.time()
    print("start")
    await login()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time} seconds")


asyncio.run(main())
