from pages.base_page import BasePage
from datetime import datetime, timedelta

class HomePage(BasePage):
    async def accept_cookies_if_present(self):
        try:
            await self.page.get_by_role("button", name="Accept").click(timeout=3000)
        except:
            pass  # no cookie popup, continue

    async def search_apartment(self, location: str, checkin_date: str = None, checkout_date: str = None, adults: int = 2, children: int = 0):
        await self.accept_cookies_if_present()

        # Fill in location
        await self.page.get_by_placeholder("Search destinations").click()
        await self.page.get_by_placeholder("Search destinations").fill(location)
        await self.page.wait_for_selector('div[role="option"] >> text=Tel Aviv')
        await self.page.locator('div[role="option"] >> text=Tel Aviv').first.click()

        # Take screenshot before opening calendar
        await self.page.screenshot(path="before_calendar.png")
        
        print("📅 Working with calendar...")
        try:
            # Instead of clicking "Add dates", try directly interacting with the calendar
            # that appears to already be visible in your screenshot
            
            # First, make sure we're on the Dates tab if it's not already selected
            try:
                dates_tab = self.page.locator('button:has-text("Dates"):not([aria-selected="true"])')
                if await dates_tab.count() > 0:
                    await dates_tab.click()
                    print("Clicked on Dates tab")
                    await self.page.wait_for_timeout(1000)
            except Exception as e:
                print(f"Note: Dates tab might already be selected: {e}")
            
            await self.page.screenshot(path="calendar_view.png")
            
            # Try to identify specific days in the calendar by their text content
            # Based on your screenshot, we can see May 17 and other dates clearly
            
            # First, try clicking on May 17
            try:
                # Get all buttons with text "17" that aren't disabled
                day_17_buttons = self.page.locator('table td button:has-text("17"):not([disabled])')
                count = await day_17_buttons.count()
                print(f"Found {count} buttons with text '17'")
                
                if count > 0:
                    # Click the first one (May 17)
                    await day_17_buttons.first.click()
                    print("Clicked on day 17")
                else:
                    # If we can't find 17, try any visible day number in the first table (May)
                    for day in ["18", "19", "20", "21", "22", "23", "24"]:
                        day_button = self.page.locator(f'table:first-of-type td button:has-text("{day}"):not([disabled])')
                        if await day_button.count() > 0:
                            await day_button.first.click()
                            print(f"Clicked on day {day} instead")
                            break
            except Exception as e:
                print(f"Error clicking first date: {e}")
                # Last resort: try to click any visible date in the calendar
                try:
                    await self.page.click('button[data-testid="calendar-day"]:not([disabled])', timeout=5000)
                    print("Clicked first available date as fallback")
                except Exception as e2:
                    print(f"Fallback also failed: {e2}")
            
            await self.page.wait_for_timeout(2000)
            await self.page.screenshot(path="after_first_date.png")
            
            # Now, try to select a second date (about a week later)
            try:
                # Try clicking on May 24 (a week after May 17)
                day_24_buttons = self.page.locator('table td button:has-text("24"):not([disabled])')
                count = await day_24_buttons.count()
                print(f"Found {count} buttons with text '24'")
                
                if count > 0:
                    # Click the first one (May 24)
                    await day_24_buttons.first.click()
                    print("Clicked on day 24")
                else:
                    # If we can't find 24, try any later day number
                    for day in ["25", "26", "27", "28", "29", "30", "31"]:
                        day_button = self.page.locator(f'table:first-of-type td button:has-text("{day}"):not([disabled])')
                        if await day_button.count() > 0:
                            await day_button.first.click()
                            print(f"Clicked on day {day} instead")
                            break
            except Exception as e:
                print(f"Error clicking second date: {e}")
                # Last resort: try to click any visible date in the calendar that might be different from the first
                try:
                    all_dates = self.page.locator('button[data-testid="calendar-day"]:not([disabled])')
                    count = await all_dates.count()
                    if count > 1:
                        await all_dates.nth(1).click()
                        print("Clicked second available date as fallback")
                except Exception as e2:
                    print(f"Second date fallback also failed: {e2}")
            
            await self.page.wait_for_timeout(2000)
            await self.page.screenshot(path="after_second_date.png")
            
            # Now look for a button to confirm the date selection
            try:
                for selector in [
                    'button:has-text("Save")',
                    'button:has-text("Apply")',
                    'button[data-testid="structured-search-input-search-button"]'
                ]:
                    button = self.page.locator(selector)
                    if await button.count() > 0:
                        await button.click()
                        print(f"Clicked confirm button with selector: {selector}")
                        break
                else:
                    # If no button was found, try pressing Enter
                    await self.page.keyboard.press("Enter")
                    print("Pressed Enter to confirm dates")
            except Exception as e:
                print(f"Error confirming date selection: {e}")
            
            await self.page.wait_for_timeout(2000)
            
        except Exception as e:
            print(f"Calendar interaction error: {e}")
            await self.page.screenshot(path="calendar_error.png")

        

        print("Setting exactly 2 adults...")
        try:
            # Click on the "Who" or "Add guests" field to open the guest selector
            try:
                # Try clicking the "Add guests" button
                await self.page.click('button:has-text("Add guests")', timeout=5000)
                print("Clicked on 'Add guests' button")
            except Exception as e:
                print(f"Couldn't click 'Add guests': {e}")
                try:
                    # Try alternative selector
                    await self.page.click('div:has-text("Who") >> button', timeout=5000)
                    print("Clicked on 'Who' section")
                except Exception as e2:
                    print(f"Couldn't click 'Who' section: {e2}")
                    # One more try
                    await self.page.click('[data-testid="structured-search-input-field-guests-button"]', timeout=5000)
                    print("Clicked on guests field with testid")
            
            # Wait for guest menu to appear
            await self.page.wait_for_timeout(2000)
            await self.page.screenshot(path="guest_menu_open.png")
            
            # Reset to a known state first - set adults to 0 if possible
            try:
                # Find the decrease button
                decrease_button = self.page.locator('[data-testid="stepper-adults-decrease-button"]').first
                
                # Click it multiple times to reset to 0 or minimum value
                for _ in range(5):  # Try up to 5 times to ensure we get to minimum
                    if await decrease_button.is_enabled():
                        await decrease_button.click()
                        await self.page.wait_for_timeout(500)
                    else:
                        break  # Button is disabled, we're at minimum
                
                print("Reset adults count to minimum")
            except Exception as e:
                print(f"Could not reset adults count: {e}")
            
            # Now increase exactly twice to get to 2 adults, regardless of starting value
            try:
                # Find the increase button
                increase_button = self.page.locator('[data-testid="stepper-adults-increase-button"]').first
                
                # Click exactly twice
                print("Clicking increase adults button exactly twice")
                await increase_button.click()
                await self.page.wait_for_timeout(1000)  # Wait between clicks
                
                # await increase_button.click()
                # await self.page.wait_for_timeout(1000)
                
                # Take a screenshot to verify
                await self.page.screenshot(path="adults_set_to_2.png")
            except Exception as e:
                print(f"Error setting adults to 2: {e}")
                
                # JavaScript approach as fallback
                try:
                    print("Trying JavaScript approach")
                    await self.page.evaluate('''
                        // First try to reset to minimum
                        const decreaseButtons = document.querySelectorAll('[data-testid="stepper-adults-decrease-button"]');
                        if (decreaseButtons.length > 0) {
                            // Click multiple times to ensure minimum
                            for (let i = 0; i < 5; i++) {
                                if (!decreaseButtons[0].disabled) {
                                    decreaseButtons[0].click();
                                } else {
                                    break;
                                }
                            }
                            
                            // Then click increase exactly twice after a delay
                            setTimeout(() => {
                                const increaseButtons = document.querySelectorAll('[data-testid="stepper-adults-increase-button"]');
                                if (increaseButtons.length > 0) {
                                    increaseButtons[0].click();
                                    setTimeout(() => increaseButtons[0].click(), 500);
                                }
                            }, 1000);
                        }
                    ''')
                    await self.page.wait_for_timeout(3000)  # Wait for JS to complete
                    print("Used JavaScript to set adults to 2")
                except Exception as e2:
                    print(f"JavaScript approach also failed: {e2}")
            
            # Click Save button to confirm guest selection
            try:
                save_button = self.page.locator('button:has-text("Save")').first
                await save_button.click(timeout=5000)
                print("Clicked Save button")
            except Exception as e:
                print(f"Error clicking Save button: {e}")
                try:
                    # Try Enter key
                    await self.page.keyboard.press("Enter")
                    print("Pressed Enter key to save")
                except Exception as e2:
                    print(f"Enter key also failed: {e2}")
            
            await self.page.wait_for_timeout(2000)
            
        except Exception as e:
            print(f"Overall error in guest selection: {e}")
            await self.page.screenshot(path="guest_selection_error.png")

        # Now click the Search button to submit the search
        print("Submitting search...")
        try:
            # Click the main search button
            search_button = self.page.locator('button[data-testid="structured-search-input-search-button"]')
            if await search_button.count() > 0:
                await search_button.click()
                print("Clicked main search button")
            else:
                # Try alternative search button selectors
                for selector in ['button:has-text("Search")', 'button[type="submit"]']:
                    button = self.page.locator(selector)
                    if await button.count() > 0:
                        await button.click()
                        print(f"Clicked search with selector: {selector}")
                        break
                else:
                    print("No search button found, trying Enter key")
                    await self.page.keyboard.press("Enter")
        except Exception as e:
            print(f"Error clicking search button: {e}")
            await self.page.screenshot(path="search_button_error.png")

        # Wait for the search results to load
        print("Waiting for search results...")
        await self.page.wait_for_timeout(5000)
        await self.page.screenshot(path="search_results.png")

        # Now click the Search button to submit the search
        # print("Submitting search...")
        # try:
        #     # Click the main search button
        #     await self.page.click('button[data-testid="structured-search-input-search-button"]', timeout=5000)
        #     print("Clicked main search button")
        # except Exception as e:
        #     print(f"Couldn't click main search button: {e}")
        #     try:
        #         # Try alternative search button selectors
        #         for selector in ['button:has-text("Search")', 'button[type="submit"]']:
        #             button = self.page.locator(selector)
        #             if await button.count() > 0:
        #                 await button.click()
        #                 print(f"Clicked search with selector: {selector}")
        #                 break
        #         else:
        #             print("No search button found, trying Enter key")
        #             await self.page.keyboard.press("Enter")
        #     except Exception as e2:
        #         print(f"Alternative search button also failed: {e2}")

        # # Wait for the search results to load
        # print("Waiting for search results...")
        # await self.page.wait_for_timeout(5000)
        # await self.page.screenshot(path="search_results.png")
        
        # Submit search
        print("Submitting search...")
        try:
            search_button = self.page.get_by_role("button", name="Search")
            await search_button.click()
            print("✅ Search submitted")
        except Exception as e:
            print(f"Search submission error: {e}")
            # Try alternative search button
            try:
                await self.page.click('button[type="submit"], button:has-text("Search")')
            except Exception as e2:
                print(f"Alternative search button error: {e2}")
                # Take a screenshot of the final state
                await self.page.screenshot(path="final_state.png")

        # Handle children count if needed
        if children > 0:
            try:
                print(f"Setting children count to {children}...")
                
                # Find and reset children count first if needed
                try:
                    decrease_button = self.page.locator('[data-testid="stepper-children-decrease-button"]').first
                    for _ in range(5):  # Try up to 5 times to reset
                        if await decrease_button.is_enabled():
                            await decrease_button.click()
                            await self.page.wait_for_timeout(500)
                        else:
                            break  # At minimum
                except Exception as e:
                    print(f"Could not reset children count: {e}")
                
                # Now increase to the desired number
                increase_button = self.page.locator('[data-testid="stepper-children-increase-button"]').first
                for _ in range(children):
                    await increase_button.click()
                    await self.page.wait_for_timeout(500)
                
                print(f"Children count set to {children}")
                await self.page.screenshot(path=f"children_set_to_{children}.png")
                
                # If adding children, sometimes there's an age selector that appears
                try:
                    # Check if age selector is present
                    age_selector = self.page.locator('select[id*="children-age"], [data-testid="children-age-select"]')
                    if await age_selector.count() > 0:
                        print("Setting children age...")
                        # Try to select middle age range (e.g., 6)
                        await age_selector.select_option('6')
                        print("Selected age 6 for children")
                    else:
                        print("No age selector found for children")
                except Exception as e:
                    print(f"Error setting children age: {e}")
            except Exception as e:
                print(f"Error setting children count: {e}")