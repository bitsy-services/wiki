---
title: "Chainlink Automation Registration"
weight: 2
---

Registration is the process of creating a new upkeep in [Chainlink Automation](automation). A registered upkeep tells the Automation network what contract to monitor, what conditions to check, and how much [LINK](https://en.wikipedia.org/wiki/Chainlink_(blockchain)#LINK_token) to allocate for execution costs.

## Registration Methods

### UI Registration

The simplest path. Go to [automation.chain.link](https://automation.chain.link/), connect a wallet, and follow the guided flow. The UI handles LINK approval, [registrar](registrar) interaction, and parameter encoding behind the scenes.

Good for one-off upkeeps and initial experimentation.

### Programmatic Registration

For automated deployments or contracts that need to self-register, call the [registrar](registrar) contract directly from Solidity or an off-chain script.

```solidity
import {IAutomationRegistrar} from "@chainlink/contracts/src/v0.8/automation/interfaces/IAutomationRegistrar.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

using SafeERC20 for IERC20;

IERC20 link = IERC20(LINK_ADDRESS);
IAutomationRegistrar registrar = IAutomationRegistrar(REGISTRAR_ADDRESS);

RegistrationParams memory params = RegistrationParams({
    name: "My Upkeep",
    encryptedEmail: "",
    upkeepContract: address(myContract),
    gasLimit: 500_000,
    adminAddress: msg.sender,
    triggerType: 0, // 0 = conditional, 1 = log trigger
    checkData: "",
    triggerConfig: "",
    offchainConfig: "",
    amount: 5 ether // 5 LINK
});

link.safeApprove(address(registrar), params.amount);
uint256 upkeepId = registrar.registerUpkeep(params);
```

### Ethers.js / Off-Chain Script

```javascript
const registrar = new ethers.Contract(REGISTRAR_ADDRESS, registrarAbi, signer);
const link = new ethers.Contract(LINK_ADDRESS, erc20Abi, signer);

const amount = ethers.parseEther("5");
await link.approve(REGISTRAR_ADDRESS, amount);

const tx = await registrar.registerUpkeep({
  name: "My Upkeep",
  encryptedEmail: "0x",
  upkeepContract: myContractAddress,
  gasLimit: 500_000,
  adminAddress: await signer.getAddress(),
  triggerType: 0,
  checkData: "0x",
  triggerConfig: "0x",
  offchainConfig: "0x",
  amount,
});

const receipt = await tx.wait();
```

## Registration Parameters

| Parameter | Purpose |
|---|---|
| `name` | Human-readable label shown in the Automation dashboard. |
| `upkeepContract` | Address of the contract implementing `checkUpkeep` / `performUpkeep`. |
| `gasLimit` | Max gas for `performUpkeep`. Set high enough for worst-case; unused gas is not charged. |
| `adminAddress` | Wallet that can modify, fund, pause, or cancel the upkeep later. |
| `triggerType` | `0` for conditional (custom logic), `1` for log trigger. |
| `checkData` | Arbitrary bytes passed to `checkUpkeep` — useful for parameterizing a single contract across multiple upkeeps. |
| `amount` | Initial LINK funding in wei. 5 LINK is a reasonable starting point for testing. |

## Auto-Approval vs Pending

Some network/registrar configurations auto-approve registrations immediately. Others place the upkeep in a **pending** state until a registry admin approves it. The Automation UI shows pending upkeeps and their status.

If your registration appears stuck in pending, check:

- The registrar's auto-approve settings for your trigger type.
- Whether the LINK amount meets the minimum threshold.

## After Registration

Once registered, you interact with the **[registry](registry)** (not the registrar) for ongoing operations:

- **Fund** — send additional LINK to keep the upkeep running.
- **Pause / Unpause** — temporarily halt execution without losing configuration.
- **Cancel** — deregister the upkeep and withdraw remaining LINK (after a cooldown period).
- **Update gas limit or check data** — reconfigure without re-registering.

## Further Reading

- [Chainlink Docs — Register an Upkeep](https://docs.chain.link/chainlink-automation/guides/register-upkeep)
- [Automation-Compatible Contract Reference](https://docs.chain.link/chainlink-automation/guides/compatible-contracts)
- [Automation Dashboard](https://automation.chain.link/)
