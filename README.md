# CoPilotTest

## Sales Order Lifecycle Batch Job – D365 FNO

This repository also contains a D365 Finance and Operations (FNO) batch job that drives all open Sales Orders through their full lifecycle automatically.

---

### Batch Job: `SalesOrderLifeCycleBatch`

**File:** `AxClass/SalesOrderLifeCycleBatch.xml`

Processes every Sales Order that is in the **Open** state through three sequential steps:

| Step | D365 FNO Operation | `DocumentStatus` |
|---|---|---|
| 1 | Confirmation | `Confirmation` |
| 2 | Picking List | `PickingList` |
| 3 | Invoice | `Invoice` |

**Error handling (acceptance criteria):**
Any failure during processing of an individual Sales Order is caught, the partial work for *that order only* is rolled back via `ttsabort`, a warning is written to the infolog, and processing continues for all remaining orders.

#### How to Schedule

1. Go to **System administration > Batch jobs > Batch jobs**.
2. Click **New** and search for `SalesOrderLifeCycleBatch`.
3. Configure recurrence and active period as required.
4. Click **OK** to save and enqueue.

---

### Tests: `SalesOrderLifeCycleBatchTest` + `SalesOrderLifeCycleBatchStub`

**Files:**
- `AxClass/SalesOrderLifeCycleBatchTest.xml` – 16 `SysTestCase` test methods
- `AxClass/SalesOrderLifeCycleBatchStub.xml` – Test double that overrides DB interaction

| ID | Test Method | What it verifies |
|---|---|---|
| TC-01 | `testSingleOpenOrderIsFullyProcessed` | A single open order passes all three steps |
| TC-02 | `testMultipleOpenOrdersAreAllProcessed` | All open orders are processed when none fail |
| TC-03 | `testFailingOrderDoesNotBlockOtherOrders` | A failing order does not prevent others from completing *(acceptance criteria)* |
| TC-04 | `testOnlyOpenOrdersAreSelected` | Only open orders are picked up; confirmed/invoiced orders are skipped |
| TC-05 | `testConfirmStepUsesCorrectDocumentStatus` | Confirmation step uses `DocumentStatus::Confirmation` |
| TC-06 | `testPickingListStepUsesCorrectDocumentStatus` | Picking list step uses `DocumentStatus::PickingList` |
| TC-07 | `testInvoiceStepUsesCorrectDocumentStatus` | Invoice step uses `DocumentStatus::Invoice` |
| TC-08 | `testConfirmThrowsWhenOrderNotFound` | `confirmSalesOrder` throws when the order does not exist |
| TC-09 | `testPickingListThrowsWhenOrderNotFound` | `processPickingList` throws when the order does not exist |
| TC-10 | `testInvoiceThrowsWhenOrderNotFound` | `invoiceSalesOrder` throws when the order does not exist |
| TC-11 | `testInfologContainsSuccessMessageForProcessedOrder` | Infolog contains a success message referencing the Sales Order Id |
| TC-12 | `testInfologContainsWarningForFailedOrder` | Infolog contains a warning referencing the failed Sales Order Id |
| TC-13 | `testBatchSummaryReportsCorrectCounts` | Summary message shows correct processed / failed counts |
| TC-14 | `testUpdateConflictIsCaughtAndBatchContinues` | `UpdateConflict` exceptions are caught and do not abort the batch |
| TC-15 | `testCanGoBatchJournalReturnsTrue` | `canGoBatchJournal()` returns `true` |
| TC-16 | `testDescriptionIsNotEmpty` | `description()` returns a non-empty label string |

#### How to Run Tests

1. Open the D365 FNO development environment (Visual Studio with the Dynamics 365 SDK).
2. In **Solution Explorer**, right-click `SalesOrderLifeCycleBatchTest` → **Run Tests**.
3. Alternatively use the **Test Explorer** (`Test > Test Explorer`) and filter by `SalesOrderLifeCycleBatchTest`.

---

## Enable User Access to AR Module – Sales Order Form in D365 FNO

This repository contains D365 Finance and Operations (FNO) security configuration artifacts to enable user access to the **Sales Order Form** in the **Accounts Receivable (AR)** module.

---

### Security Artifacts

#### 1. Security Privilege – `ARSalesOrderFormAccess`
**File:** `SecurityPrivileges/ARSalesOrderFormAccess.xml`

Grants access to the following entry points:
| Entry Point | Type | Access Level |
|---|---|---|
| `SalesTableListPage` | MenuItemDisplay | Read, Update, Create, Delete, Correct |
| `SalesTable` | MenuItemDisplay | Read, Update, Create, Delete, Correct |
| `SalesTableCreate` | MenuItemAction | Read, Update, Create, Delete, Correct |

#### 2. Security Duty – `ARSalesOrderMaintain`
**File:** `SecurityDuties/ARSalesOrderMaintain.xml`

Bundles the `ARSalesOrderFormAccess` privilege into a duty that covers maintaining sales orders in the AR module.

#### 3. Security Role – `ARSalesOrderUser`
**File:** `SecurityRoles/ARSalesOrderUser.xml`

A role that includes the `ARSalesOrderMaintain` duty, ready to be assigned to users who need access to the Sales Order form.

---

### How to Apply

1. **Import artifacts into D365 FNO:**
   - Go to **System administration > Security > Security configuration**.
   - Import the XML files in this order:
     1. `SecurityPrivileges/ARSalesOrderFormAccess.xml`
     2. `SecurityDuties/ARSalesOrderMaintain.xml`
     3. `SecurityRoles/ARSalesOrderUser.xml`

2. **Assign the role to users:**
   - Go to **System administration > Users > Users**.
   - Select the user(s) who need access.
   - Under **User's roles**, click **Assign roles** and add the **AR Sales Order User** role.

3. **Verify access:**
   - Log in as the target user and navigate to **Accounts receivable > Orders > All sales orders** to confirm access to the Sales Order form.

---

### Directory Structure

```
AxClass/
  SalesOrderLifeCycleBatch.xml      # Batch job: Sales Order lifecycle processing
  SalesOrderLifeCycleBatchStub.xml  # Test double (for automated testing only)
  SalesOrderLifeCycleBatchTest.xml  # Unit tests (16 test cases)
SecurityPrivileges/
  ARSalesOrderFormAccess.xml        # Privilege: access to Sales Order form entry points
SecurityDuties/
  ARSalesOrderMaintain.xml          # Duty: maintain sales orders
SecurityRoles/
  ARSalesOrderUser.xml              # Role: AR Sales Order User (assigned to users)
```
