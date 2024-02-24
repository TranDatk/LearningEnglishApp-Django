import {
    Modal, Form, Input, Switch, Button,
} from 'antd';
import { IUser } from './user.table';
import { registerUser } from '../../api/user.api';

interface Istate {
    isModalOpen: boolean;
    setIsModalOpen: (isModalOpen: boolean) => void;
    setIsAddSuccess: (isAddSuccess: boolean) => void;
}

// const normFile = (e: any) => {
//     if (Array.isArray(e)) {
//         return e;
//     }
//     return e?.fileList;
// };

const AddUserModal = (state: Istate) => {
    const [form] = Form.useForm<IUser>();
    state.setIsAddSuccess(false);

    const handleOk = () => {
        registerUser(form.getFieldsValue()).then((value) => {
            if (!!value) {
                state.setIsAddSuccess(true)
            }
        })
        state.setIsModalOpen(false);
    };

    return (
        <Modal
            maskClosable={false}
            title="Thêm người dùng"
            open={state.isModalOpen}
            onOk={handleOk}
            onCancel={() => state.setIsModalOpen(false)}
            footer={[
                <Button key="back" onClick={() => state.setIsModalOpen(false)}>
                    Hủy
                </Button>,
                <Button key="submit" htmlType='submit' type="primary" onClick={handleOk}>
                    Thêm mới
                </Button>,
            ]}>
            <Form
                labelCol={{ span: 5 }}
                wrapperCol={{ span: 15 }}
                layout="horizontal"
                style={{ maxWidth: 600 }}
                form={form}
                onFinish={handleOk}
            >
                <Form.Item label="Username" name="username" rules={[{ required: true }]}>
                    <Input onChange={(e) => { form.setFieldValue("username", e.target.value) }} />
                </Form.Item>
                <Form.Item label="Password1" name="password1" rules={[{ required: true }]}>
                    <Input.Password onChange={(e) => { form.setFieldValue("password1", e.target.value) }} />
                </Form.Item>
                <Form.Item label="Password2" name="password2" rules={[{ required: true }]}>
                    <Input.Password onChange={(e) => { form.setFieldValue("password2", e.target.value) }} />
                </Form.Item>
                <Form.Item label="Firstname" name="first_name" rules={[{ required: true }]}>
                    <Input onChange={(e) => { form.setFieldValue("first_name", e.target.value) }} />
                </Form.Item>
                <Form.Item label="Lastname" name="last_name" rules={[{ required: true }]}>
                    <Input onChange={(e) => { form.setFieldValue("last_name", e.target.value) }} />
                </Form.Item>
                <Form.Item label="Email" name="email" rules={[{ required: true }]}>
                    <Input onChange={(e) => { form.setFieldValue("email", e.target.value) }} />
                </Form.Item>
                <Form.Item label="is_superuser" name="is_superuser" valuePropName="checked" rules={[{ required: true }]}>
                    <Switch onChange={(e) => { form.setFieldValue("is_superuser", e) }} />
                </Form.Item>
                {/* <Form.Item label="Upload" name="avatar" valuePropName="fileList" getValueFromEvent={normFile}>
                    <Upload
                        maxCount={1}
                        listType="picture-card"
                        beforeUpload={(file) => {
                            form.setFieldValue("avatar", [file]); // Gán giá trị tệp tin cho avatar
                            return false; // Ngăn việc tải lên tự động
                        }}
                        fileList={form.getFieldValue("avatar")} // fileList của Upload sẽ được điều chỉnh từ Form
                        onChange={(info) => {
                            if (info.file.status === "done") {
                                const uploadedFile = info.file.originFileObj; // Lấy tệp tin đã được tải lên
                                form.setFieldValue("avatar", [uploadedFile]); // Gán giá trị tệp tin cho avatar khi đã hoàn thành tải lên
                            }
                        }}
                    >
                        {form.getFieldValue("avatar")?.length === 1 ? null : (
                            <div>
                                <PlusOutlined />
                                <div style={{ marginTop: 8 }}>Upload</div>
                            </div>
                        )}
                    </Upload>
                </Form.Item> */}
            </Form>
        </Modal>
    )
}

export default AddUserModal;