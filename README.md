# CoPilotTest

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
SecurityPrivileges/
  ARSalesOrderFormAccess.xml    # Privilege: access to Sales Order form entry points
SecurityDuties/
  ARSalesOrderMaintain.xml      # Duty: maintain sales orders
SecurityRoles/
  ARSalesOrderUser.xml          # Role: AR Sales Order User (assigned to users)
```
