from web3 import Web3
from eth_account import Account
import time
import sys
import os

# Detail jaringan
private_key = '0x809432675cd18adbc1df86d44e918227b82fa06ab826eae15f0e053a4a05616f' # GANTI DENGAN PRIVATE KEY ANDA
rpc_url = 'https://sepolia-rollup.arbitrum.io/rpc' # JANGAN DIGANTI
chain_id = 421614 # JANGAN DIGANTI
contract_address = '0x8D86c3573928CE125f9b2df59918c383aa2B514D' # JANGAN DIGANTI
my_address = '0xb283ec154eBF6eB248E8E6cFB523Aa40ae617334' # GANTI DENGAN ADDRESS EVM ANDA

# Koneksi ke jaringan
web3 = Web3(Web3.HTTPProvider(rpc_url))
if not web3.is_connected():
    raise Exception("Tidak dapat terhubung ke jaringan")

# Buat akun dari private key
account = Account.from_key(private_key)

# Data transaksi untuk bridge ( Jangan Diganti )
data = '0xf735544df69f32eac166fcce4f39dc2dcc9f3678f2e15e8c51ce5b049cae58722de98bf1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000005af3107a400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000066d8734a'

# Fungsi untuk membuat dan mengirim transaksi
def send_bridge_transaction():
    # Ambil nonce untuk alamat pengirim
    nonce = web3.eth.get_transaction_count(my_address)

    # Estimasi gas
    try:
        gas_estimate = web3.eth.estimate_gas({
            'to': contract_address,
            'from': my_address,
            'data': data,
            'value': web3.to_wei(0.0001, 'ether')  # Mengirim 0.0001 ETH
        })
        gas_limit = gas_estimate + 10000  # Tambahkan buffer gas
    except Exception as e:
        print(f"Error estimating gas: {e}")
        return None

    # Buat transaksi
    transaction = {
        'nonce': nonce,
        'to': contract_address,
        'value': web3.to_wei(0.0001, 'ether'),  # Mengirim 0.0001 ETH
        'gas': gas_limit,  # Gunakan gas limit yang diestimasi
        'gasPrice': web3.eth.gas_price,
        'chainId': chain_id,
        'data': data
    }

    # Tanda tangani transaksi dengan private key
    try:
        signed_txn = web3.eth.account.sign_transaction(transaction, private_key)
    except Exception as e:
        print(f"Error signing transaction: {e}")
        return None

    # Kirim transaksi
    try:
        tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
        return web3.to_hex(tx_hash)
    except Exception as e:
        print(f"Error sending transaction: {e}")
        return None

# Jalankan script sampai dihentikan secara manual
successful_txs = 0

try:
    while True:
        tx_hash = send_bridge_transaction()
        if tx_hash:
            successful_txs += 1
            print(f"Tx Hash: {tx_hash} | Total Tx Sukses: {successful_txs}")
        time.sleep(20)  # Delay 20 detik setiap transaksi
except KeyboardInterrupt:
    print("\nScript dihentikan oleh pengguna.")
    print(f"Total transaksi sukses: {successful_txs}")
    sys.exit(0)
