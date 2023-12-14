import { useEffect, useState } from 'react';
import { getListUsers, login } from '../../api/user.api';
import type { ColumnsType } from 'antd/es/table';
import Table from 'antd/es/table';
import { CheckCircleOutlined, CloseCircleOutlined, EditOutlined, PlusCircleOutlined, DeleteOutlined } from '@ant-design/icons';
import { Space, Button, Modal } from 'antd';

interface IUser {
    id: number;
    username: string;
    first_name: string;
    last_name: string;
    avatar: string;
    email: string;
    is_superuser: boolean;
    is_active: boolean;
}

const UserTable = () => {
    const [listUsers, setListUsers] = useState([])
    const [isModalOpen, setIsModalOpen] = useState(false);

    const columns: ColumnsType<IUser> = [
        {
            title: 'Id',
            dataIndex: 'id',
            key: 'id',
        },
        {
            title: 'Username',
            dataIndex: 'username',
            key: 'username',
        },
        {
            title: 'Firstname',
            dataIndex: 'first_name',
            key: 'first_name',
        },
        {
            title: 'Lastname',
            dataIndex: 'last_name',
            key: 'last_name',
        },
        {
            title: 'Email',
            dataIndex: 'email',
            key: 'email',
        },
        {
            title: 'Avatar',
            dataIndex: 'avatar',
            key: 'avatar',
        },
        {
            title: 'is_superuser',
            dataIndex: 'is_superuser',
            key: 'is_superuser',
            render: (_, { is_superuser }) => (
                <>
                    {is_superuser && <CheckCircleOutlined style={{ color: 'green' }} />}
                    {!is_superuser && <CloseCircleOutlined style={{ color: 'red' }} />}
                </>
            ),
        },
        {
            title: 'is_active',
            dataIndex: 'is_active',
            key: 'is_active',
            render: (_, { is_active }) => (
                <>
                    {is_active && <CheckCircleOutlined style={{ color: 'green' }} />}
                    {!is_active && <CloseCircleOutlined style={{ color: 'red' }} />}
                </>
            ),
        },
        {
            title: 'Action',
            key: 'action',
            render: () => (
                <Space size="middle">
                    <Button onClick={showModal} type="primary" icon={<PlusCircleOutlined />} style={{ background: '#9ACD32' }} />
                    <Button onClick={showModal} type="default" icon={<EditOutlined />} style={{ background: '#F0E68C' }} />
                    <Button onClick={showModal} type="primary" danger icon={<DeleteOutlined />} />
                </Space>
            ),
        },
    ]


    const showModal = () => {
        setIsModalOpen(true);
    };

    const handleOk = () => {
        setIsModalOpen(false);
    };

    const handleCancel = () => {
        setIsModalOpen(false);
    };

    useEffect(() => {
        login("admin", "Admin@123")
        getListUsers().then(value => {
            setListUsers(value?.results ?? [])
        }).catch(err => {
            console.log(err);
        });
    }, [])

    console.log(listUsers)

    return (
        <>
            <h2>Danh sách người dùng</h2>
            <Table columns={columns} dataSource={listUsers} />
            <Modal title="Basic Modal" open={isModalOpen} onOk={handleOk} onCancel={handleCancel}>
                <p>Some contents...</p>
                <p>Some contents...</p>
                <p>Some contents...</p>
            </Modal>
        </>
    )
}

export default UserTable;