// tests/e2e/task-management.e2e.test.ts
import { test, expect } from '@playwright/test';

test.describe('Task Management Workflow', () => {
  test.beforeEach(async ({ page }) => {
    // Assuming the app is running on localhost:3000
    await page.goto('http://localhost:3000');
  });

  test('should allow a user to complete the full task management workflow', async ({ page }) => {
    // 1. Navigate to sign up page
    await page.getByRole('link', { name: 'Sign up' }).click();
    await expect(page).toHaveURL(/.*signup/);

    // 2. Register a new user
    const email = `testuser_${Date.now()}@example.com`;
    const password = 'SecurePassword123!';
    const name = 'Test User';

    await page.locator('[name="email"]').fill(email);
    await page.locator('[name="name"]').fill(name);
    await page.locator('[name="password"]').fill(password);
    await page.locator('[name="confirmPassword"]').fill(password);
    
    await page.getByRole('button', { name: 'Sign Up' }).click();

    // 3. Verify redirection to dashboard after sign up
    await expect(page).toHaveURL(/.*dashboard/);
    await expect(page.getByText(`Welcome, ${name}`)).toBeVisible();

    // 4. Create a new task
    const taskTitle = 'Test Task';
    const taskDescription = 'This is a test task description';
    
    await page.locator('#title').fill(taskTitle);
    await page.locator('#description').fill(taskDescription);
    await page.getByRole('button', { name: 'Add Task' }).click();

    // 5. Verify the task appears in the list
    await expect(page.getByText(taskTitle)).toBeVisible();
    await expect(page.getByText(taskDescription)).toBeVisible();

    // 6. Mark the task as completed
    const taskCheckbox = page.locator('.completion-checkbox').first();
    await taskCheckbox.click();
    
    // 7. Verify the task is marked as completed
    await expect(taskCheckbox).toBeChecked();

    // 8. Edit the task
    const editButton = page.getByRole('button', { name: 'Edit' }).first();
    await editButton.click();
    
    const newTitle = `${taskTitle} - Updated`;
    await page.locator('.edit-title').fill(newTitle);
    await page.getByRole('button', { name: 'Save' }).click();
    
    // 9. Verify the task was updated
    await expect(page.getByText(newTitle)).toBeVisible();

    // 10. Delete the task
    const deleteButton = page.getByRole('button', { name: 'Delete' }).first();
    await deleteButton.click();
    
    // 11. Verify the task is removed from the list
    await expect(page.getByText(newTitle)).not.toBeVisible();
  });

  test('should handle authentication correctly', async ({ page }) => {
    // Try to access dashboard without authentication
    await page.goto('http://localhost:3000/dashboard');
    
    // Should redirect to sign in page
    await expect(page).toHaveURL(/.*signin/);
  });
});

test.describe('Chat-Based Task Management', () => {
  test.beforeEach(async ({ page }) => {
    // Assuming the app is running on localhost:3000
    await page.goto('http://localhost:3000');
  });

  test('should allow a user to manage tasks via chat interface', async ({ page }) => {
    // 1. Register a new user
    const email = `chatuser_${Date.now()}@example.com`;
    const password = 'SecurePassword123!';
    const name = 'Chat User';

    await page.getByRole('link', { name: 'Sign up' }).click();
    await page.locator('[name="email"]').fill(email);
    await page.locator('[name="name"]').fill(name);
    await page.locator('[name="password"]').fill(password);
    await page.locator('[name="confirmPassword"]').fill(password);
    await page.getByRole('button', { name: 'Sign Up' }).click();

    // 2. Navigate to the chat page
    await page.getByRole('link', { name: 'Chat' }).click();
    await expect(page).toHaveURL(/.*chat/);

    // 3. Ask the AI to create a task
    const taskTitle = 'Buy groceries';
    await page.locator('textarea').fill(`Add a task to ${taskTitle}`);
    await page.getByRole('button', { name: 'Send' }).click();

    // 4. Verify the AI confirms the task creation
    await expect(page.getByText(new RegExp(`.*${taskTitle}.*`, 'i'))).toBeVisible();

    // 5. Navigate to the dashboard to verify the task was created
    await page.getByRole('link', { name: 'Dashboard' }).click();
    await expect(page.getByText(taskTitle)).toBeVisible();

    // 6. Go back to chat and ask to mark the task as complete
    await page.getByRole('link', { name: 'Chat' }).click();
    await page.locator('textarea').fill(`Mark the task '${taskTitle}' as complete`);
    await page.getByRole('button', { name: 'Send' }).click();

    // 7. Verify the AI confirms the task completion
    await expect(page.getByText(new RegExp(`.*marked.*complete.*${taskTitle}.*`, 'i'))).toBeVisible();

    // 8. Go back to dashboard to verify the task is marked as completed
    await page.getByRole('link', { name: 'Dashboard' }).click();
    // Find the task and verify it's checked
    const taskItem = page.locator('.task-item').filter({ hasText: taskTitle });
    const taskCheckbox = taskItem.locator('.completion-checkbox');
    await expect(taskCheckbox).toBeChecked();
  });
});